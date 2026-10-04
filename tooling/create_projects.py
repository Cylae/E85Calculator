"""Generate aligned test vectors, native test fixtures and a regular Xcode project."""
from pathlib import Path
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]

def inp(r=35/3, rl=.05, rh=.05, target=.3, c=35, pl=.85, ph=.85, sl=.05, sh=.05):
    return dict(finalLiters=c, remainingLiters=r, residual=dict(low=rl, high=rh),
                e85=dict(low=pl, high=ph), sp98=dict(low=sl, high=sh), target=target)

vectors = [
    dict(name="E30, remaining E5, 2/6 assumption", input=inp(),
         expected=dict(feasible=True,exactE85Liters=10.9375,e85Liters=10.93,sp98Liters=35*2/3-10.93,minimumUpper=.05)),
    dict(name="E30, remaining E50", input=inp(rl=.5,rh=.5),
         expected=dict(feasible=True,exactE85Liters=4.375,e85Liters=4.37,sp98Liters=35*2/3-4.37,minimumUpper=.2)),
    dict(name="E30 impossible with remaining E85", input=inp(rl=.85,rh=.85),
         expected=dict(feasible=False,exactE85Liters=None,e85Liters=None,sp98Liters=None,minimumUpper=19/60)),
    dict(name="Unknown remaining mixture, E10 cannot be guaranteed", input=inp(rl=0,rh=.85,target=.1,pl=.54,sl=0),
         expected=dict(feasible=False,exactE85Liters=None,e85Liters=None,sp98Liters=None,minimumUpper=19/60)),
    dict(name="E10 with remaining E5", input=inp(target=.1),
         expected=dict(feasible=True,exactE85Liters=2.1875,e85Liters=2.18,sp98Liters=35*2/3-2.18,minimumUpper=.05)),
    dict(name="Empty tank to E30", input=inp(r=0),
         expected=dict(feasible=True,exactE85Liters=10.9375,e85Liters=10.93,sp98Liters=24.07,minimumUpper=.05)),
    dict(name="Empty tank full E85 is constrained by space", input=inp(r=0,target=1,pl=.54,sl=0),
         expected=dict(feasible=True,exactE85Liters=35,e85Liters=35,sp98Liters=0,minimumUpper=.05)),
    dict(name="Full tank below the chosen ceiling", input=inp(r=35,target=.1),
         expected=dict(feasible=True,exactE85Liters=0,e85Liters=0,sp98Liters=0,minimumUpper=.05)),
    dict(name="E5 ceiling with E5 remaining", input=inp(target=.05),
         expected=dict(feasible=True,exactE85Liters=0,e85Liters=0,sp98Liters=35*2/3,minimumUpper=.05)),
    dict(name="Zero ethanol ceiling, all E0", input=inp(r=0,rl=0,rh=0,target=0,sl=0,sh=0),
         expected=dict(feasible=True,exactE85Liters=0,e85Liters=0,sp98Liters=35,minimumUpper=0)),
    dict(name="Out-of-range remaining volume", input=inp(r=36), error=True),
    dict(name="Zero final volume", input=inp(r=0,c=0), error=True),
    dict(name="Negative remaining volume", input=inp(r=-1), error=True),
    dict(name="Reversed residual interval", input=inp(rl=.5,rh=.4), error=True),
    dict(name="Fraction above one", input=inp(rh=1.1), error=True),
    dict(name="Identical source upper bounds", input=inp(pl=.05,ph=.05), error=True),
    dict(name="Overlapping source intervals", input=inp(pl=.01), error=True),
    dict(name="Negative target", input=inp(target=-.1), error=True),
]
(ROOT / "verification/test_vectors.json").write_text(json.dumps(vectors,ensure_ascii=False,indent=2)+"\n")

def kotlin_input(v):
    a=v["input"]
    return "BlendInput(" + ", ".join([repr(a['finalLiters'])+".0" if isinstance(a['finalLiters'],int) else repr(a['finalLiters']),
        repr(float(a['remainingLiters'])),
        *[f"FractionRange({float(a[k]['low'])}, {float(a[k]['high'])})" for k in ('residual','e85','sp98')],repr(float(a['target']))])+ ")"

kt='''package com.cylae.aygoblend
import org.junit.Assert.*
import org.junit.Test

class BlendEngineTest {
'''
for i,v in enumerate(vectors):
    kt+=f'    @Test fun case{i:02d}() {{\n        val input = {kotlin_input(v)}\n'
    if v.get("error"):
        kt+='        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(input) }\n'
    else:
        e=v['expected']; kt+='        val result = BlendEngine.calculate(input)\n'
        kt+=f"        assertEquals({str(e['feasible']).lower()}, result.feasible)\n"
        for k in ('exactE85Liters','e85Liters','sp98Liters','minimumUpper'):
            if e[k] is None: kt+=f"        assertNull(result.{k})\n"
            else: kt+=f"        assertEquals({float(e[k])}, result.{k}{'!!' if k != 'minimumUpper' else ''}, 1e-8)\n"
    kt+='    }\n'
kt+='''    @Test fun decimalParsing() {
        assertEquals(1.25, BlendEngine.parseDecimal("1,25")!!, 1e-12)
        for (s in listOf("", "NaN", "Infinity", "1e4", "1,2.3", "0x10")) assertNull(BlendEngine.parseDecimal(s))
    }
    @Test fun rejectsNonFinite() {
        val bad = BlendInput(Double.NaN, 0.0, FractionRange(0.0,0.0), FractionRange(.54,.85), FractionRange(0.0,.05), .1)
        assertThrows(IllegalArgumentException::class.java) { BlendEngine.calculate(bad) }
    }
}
'''
p=ROOT/'android/app/src/test/java/com/cylae/aygoblend/BlendEngineTest.kt';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(kt)

sw='''import XCTest
@testable import AygoBlend

final class BlendEngineTests: XCTestCase {
'''
for i,v in enumerate(vectors):
    a=v['input']; names=('finalLiters','remainingLiters','residual','e85','sp98','target')
    args=[]
    for k in names:
        val=a[k]
        args.append(f"{k}: "+(f"FractionRange(low: {val['low']}, high: {val['high']})" if isinstance(val,dict) else repr(val)))
    sw+=f"    func testCase{i:02d}() throws {{\n        let input = BlendInput({', '.join(args)})\n"
    if v.get('error'): sw+='        XCTAssertThrowsError(try BlendEngine.calculate(input))\n'
    else:
        e=v['expected'];sw+='        let result = try BlendEngine.calculate(input)\n'
        sw+=f"        XCTAssertEqual(result.feasible, {str(e['feasible']).lower()})\n"
        for k in ('exactE85Liters','e85Liters','sp98Liters','minimumUpper'):
            if e[k] is None:sw+=f"        XCTAssertNil(result.{k})\n"
            else: sw+=f"        XCTAssertEqual({'try XCTUnwrap(result.'+k+')' if k != 'minimumUpper' else 'result.'+k}, {e[k]}, accuracy: 1e-8)\n"
    sw+='    }\n'
sw+='''    func testDecimalParsing() {
        XCTAssertEqual(BlendEngine.parseDecimal("1,25"), 1.25)
        for s in ["", "NaN", "Infinity", "1e4", "1,2.3", "0x10"] { XCTAssertNil(BlendEngine.parseDecimal(s)) }
    }
    func testNonFinite() {
        let bad = BlendInput(finalLiters: .nan, remainingLiters: 0, residual: FractionRange(low:0,high:0),
            e85: FractionRange(low:0.54,high:0.85), sp98: FractionRange(low:0,high:0.05), target:0.1)
        XCTAssertThrowsError(try BlendEngine.calculate(bad))
    }
}
'''
p=ROOT/'ios/AygoBlendTests/BlendEngineTests.swift';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(sw)

def uid(name): return hashlib.sha256(name.encode()).hexdigest()[:24].upper()
def quoted(s): return json.dumps(s)
objects=[]
def obj(name, body): objects.append(f"\t\t{uid(name)} = {{ {body} }};"); return uid(name)
file_refs=[]; app_build=[]
for name in ('AygoBlendApp.swift','ContentView.swift','BlendEngine.swift'):
    ref=obj('file/'+name,f'isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = {quoted(name)}; sourceTree = "<group>";')
    file_refs.append(ref);app_build.append(obj('build/'+name,f'isa = PBXBuildFile; fileRef = {ref};'))
test_ref=obj('testfile','isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = BlendEngineTests.swift; sourceTree = "<group>";')
test_build=obj('testbuild',f'isa = PBXBuildFile; fileRef = {test_ref};')
app_product=obj('app-product','isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = AygoBlend.app; sourceTree = BUILT_PRODUCTS_DIR;')
test_product=obj('test-product','isa = PBXFileReference; explicitFileType = wrapper.cfbundle; includeInIndex = 0; path = AygoBlendTests.xctest; sourceTree = BUILT_PRODUCTS_DIR;')
app_group=obj('app-group',f'isa = PBXGroup; children = ({", ".join(file_refs)},); path = AygoBlend; sourceTree = "<group>";')
test_group=obj('test-group',f'isa = PBXGroup; children = ({test_ref},); path = AygoBlendTests; sourceTree = "<group>";')
products=obj('products',f'isa = PBXGroup; children = ({app_product},{test_product},); name = Products; sourceTree = "<group>";')
main=obj('main-group',f'isa = PBXGroup; children = ({app_group},{test_group},{products},); sourceTree = "<group>";')
app_sources=obj('app-sources',f'isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = ({", ".join(app_build)},); runOnlyForDeploymentPostprocessing = 0;')
test_sources=obj('test-sources',f'isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = ({test_build},); runOnlyForDeploymentPostprocessing = 0;')
app_frameworks=obj('app-frameworks','isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')
test_frameworks=obj('test-frameworks','isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')
resources=obj('resources','isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')
config_ids={}
for scope in ('project','app','tests'):
    config_ids[scope]=[]
    for mode in ('Debug','Release'):
        settings=dict(SWIFT_VERSION='5.0',IPHONEOS_DEPLOYMENT_TARGET='16.0',SDKROOT='iphoneos',
            CLANG_ENABLE_MODULES='YES',CODE_SIGN_STYLE='Automatic')
        if mode=='Debug':settings.update(SWIFT_OPTIMIZATION_LEVEL='-Onone',ENABLE_TESTABILITY='YES')
        else:settings.update(SWIFT_OPTIMIZATION_LEVEL='-O')
        if scope=='app':settings.update(PRODUCT_BUNDLE_IDENTIFIER='com.cylae.aygoblend',PRODUCT_NAME='$(TARGET_NAME)',
            GENERATE_INFOPLIST_FILE='YES',INFOPLIST_KEY_UILaunchScreen_Generation='YES',
            INFOPLIST_KEY_UIApplicationSceneManifest_Generation='YES',TARGETED_DEVICE_FAMILY='1,2',
            MARKETING_VERSION='0.1.0',CURRENT_PROJECT_VERSION='1')
        if scope=='tests':settings.update(PRODUCT_BUNDLE_IDENTIFIER='com.cylae.aygoblend.tests',PRODUCT_NAME='$(TARGET_NAME)',
            GENERATE_INFOPLIST_FILE='YES',TEST_HOST='$(BUILT_PRODUCTS_DIR)/AygoBlend.app/$(BUNDLE_EXECUTABLE_FOLDER_PATH)/AygoBlend',
            BUNDLE_LOADER='$(TEST_HOST)',TARGETED_DEVICE_FAMILY='1,2')
        body=' '.join(f'{k} = {quoted(v)};' for k,v in settings.items())
        config_ids[scope].append(obj(f'{scope}/{mode}',f'isa = XCBuildConfiguration; buildSettings = {{ {body} }}; name = {mode};'))
    obj(scope+'-config-list',f'isa = XCConfigurationList; buildConfigurations = ({", ".join(config_ids[scope])},); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;')
proxy=obj('proxy',f'isa = PBXContainerItemProxy; containerPortal = {uid("project")}; proxyType = 1; remoteGlobalIDString = {uid("app-target")}; remoteInfo = AygoBlend;')
dependency=obj('dependency',f'isa = PBXTargetDependency; target = {uid("app-target")}; targetProxy = {proxy};')
app_target=obj('app-target',f'isa = PBXNativeTarget; buildConfigurationList = {uid("app-config-list")}; buildPhases = ({app_sources},{app_frameworks},{resources},); buildRules = (); dependencies = (); name = AygoBlend; productName = AygoBlend; productReference = {app_product}; productType = "com.apple.product-type.application";')
test_target=obj('test-target',f'isa = PBXNativeTarget; buildConfigurationList = {uid("tests-config-list")}; buildPhases = ({test_sources},{test_frameworks},); buildRules = (); dependencies = ({dependency},); name = AygoBlendTests; productName = AygoBlendTests; productReference = {test_product}; productType = "com.apple.product-type.bundle.unit-test";')
project=obj('project',f'isa = PBXProject; attributes = {{ LastUpgradeCheck = 1600; TargetAttributes = {{ {app_target} = {{ CreatedOnToolsVersion = 16.0; }}; {test_target} = {{ CreatedOnToolsVersion = 16.0; TestTargetID = {app_target}; }}; }}; }}; buildConfigurationList = {uid("project-config-list")}; compatibilityVersion = "Xcode 14.0"; developmentRegion = en; hasScannedForEncodings = 0; knownRegions = (en,Base,); mainGroup = {main}; productRefGroup = {products}; projectDirPath = ""; projectRoot = ""; targets = ({app_target},{test_target},);')
p=ROOT/'ios/AygoBlend.xcodeproj/project.pbxproj';p.parent.mkdir(parents=True,exist_ok=True)
p.write_text('// !$*UTF8*$!\n{\n\tarchiveVersion = 1;\n\tclasses = {};\n\tobjectVersion = 56;\n\tobjects = {\n'+ '\n'.join(objects)+'\n\t};\n\trootObject = '+project+';\n}\n')
scheme=f'''<?xml version="1.0" encoding="UTF-8"?>
<Scheme LastUpgradeVersion="1600" version="1.7">
  <BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES"><BuildActionEntries>
    <BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES">
      <BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{app_target}" BuildableName="AygoBlend.app" BlueprintName="AygoBlend" ReferencedContainer="container:AygoBlend.xcodeproj"/>
    </BuildActionEntry>
  </BuildActionEntries></BuildAction>
  <TestAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.DebuggerFoundation.Launcher.LLDB" shouldUseLaunchSchemeArgsEnv="YES"><Testables>
    <TestableReference skipped="NO"><BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{test_target}" BuildableName="AygoBlendTests.xctest" BlueprintName="AygoBlendTests" ReferencedContainer="container:AygoBlend.xcodeproj"/></TestableReference>
  </Testables></TestAction>
  <LaunchAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.DebuggerFoundation.Launcher.LLDB" launchStyle="0" useCustomWorkingDirectory="NO" ignoresPersistentStateOnLaunch="NO" debugServiceExtension="internal" allowLocationSimulation="YES">
    <BuildableProductRunnable runnableDebuggingMode="0"><BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{app_target}" BuildableName="AygoBlend.app" BlueprintName="AygoBlend" ReferencedContainer="container:AygoBlend.xcodeproj"/></BuildableProductRunnable>
  </LaunchAction>
  <ProfileAction buildConfiguration="Release" shouldUseLaunchSchemeArgsEnv="YES" savedToolIdentifier="" useCustomWorkingDirectory="NO" debugServiceExtension="internal"/>
  <AnalyzeAction buildConfiguration="Debug"/><ArchiveAction buildConfiguration="Release" revealArchiveInOrganizer="YES"/>
</Scheme>
'''
p=ROOT/'ios/AygoBlend.xcodeproj/xcshareddata/xcschemes/AygoBlend.xcscheme';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(scheme)
print(json.dumps(dict(vectors=len(vectors),androidTests=len(vectors)+2,iosTests=len(vectors)+2,xcodeProject=str(ROOT/'ios/AygoBlend.xcodeproj'))))
