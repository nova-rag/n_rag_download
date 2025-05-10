





<!DOCTYPE html>
<html class="gl-light ui-neutral with-top-bar with-header " lang="en">
<head prefix="og: http://ogp.me/ns#">
<meta charset="utf-8">
<meta content="IE=edge" http-equiv="X-UA-Compatible">
<meta content="width=device-width, initial-scale=1" name="viewport">
<title>llvm/docs/RISCVUsage.rst · 3b75a5c4c84d17d6647ba079391722ed9be09f85 · llvm-doe / llvm-project · GitLab</title>
<script>
//<![CDATA[
window.gon={};gon.math_rendering_limits_enabled=true;gon.features={"inlineBlame":false,"blobOverflowMenu":false,"blobRepositoryVueHeaderApp":false};gon.licensed_features={"fileLocks":true,"remoteDevelopment":true};
//]]>
</script>


<script>
//<![CDATA[
var gl = window.gl || {};
gl.startup_calls = {"/llvm-doe/llvm-project/-/blob/3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm/docs/RISCVUsage.rst?format=json\u0026viewer=rich":{}};
gl.startup_graphql_calls = [{"query":"query getBlobInfo(\n  $projectPath: ID!\n  $filePath: [String!]!\n  $ref: String!\n  $refType: RefType\n  $shouldFetchRawText: Boolean!\n) {\n  project(fullPath: $projectPath) {\n    __typename\n    id\n    repository {\n      __typename\n      empty\n      blobs(paths: $filePath, ref: $ref, refType: $refType) {\n        __typename\n        nodes {\n          __typename\n          id\n          webPath\n          name\n          size\n          rawSize\n          rawTextBlob @include(if: $shouldFetchRawText)\n          fileType\n          language\n          path\n          blamePath\n          editBlobPath\n          gitpodBlobUrl\n          ideEditPath\n          forkAndEditPath\n          ideForkAndEditPath\n          codeNavigationPath\n          projectBlobPathRoot\n          forkAndViewPath\n          environmentFormattedExternalUrl\n          environmentExternalUrlForRouteMap\n          canModifyBlob\n          canModifyBlobWithWebIde\n          canCurrentUserPushToBranch\n          archived\n          storedExternally\n          externalStorage\n          externalStorageUrl\n          rawPath\n          replacePath\n          pipelineEditorPath\n          simpleViewer {\n            fileType\n            tooLarge\n            type\n            renderError\n          }\n          richViewer {\n            fileType\n            tooLarge\n            type\n            renderError\n          }\n        }\n      }\n    }\n  }\n}\n","variables":{"projectPath":"llvm-doe/llvm-project","ref":"3b75a5c4c84d17d6647ba079391722ed9be09f85","refType":null,"filePath":"llvm/docs/RISCVUsage.rst","shouldFetchRawText":false}}];

if (gl.startup_calls && window.fetch) {
  Object.keys(gl.startup_calls).forEach(apiCall => {
   gl.startup_calls[apiCall] = {
      fetchCall: fetch(apiCall, {
        // Emulate XHR for Rails AJAX request checks
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        },
        // fetch won’t send cookies in older browsers, unless you set the credentials init option.
        // We set to `same-origin` which is default value in modern browsers.
        // See https://github.com/whatwg/fetch/pull/585 for more information.
        credentials: 'same-origin'
      })
    };
  });
}
if (gl.startup_graphql_calls && window.fetch) {
  const headers = {"X-CSRF-Token":"DW4LflqZ072oozs0gwLo_DQmc-SjpQRyfNzjJsEnxejSmo15fU2KL-RfEQgX3N9D2Lz0eZWwFutFNkUTk6s1bw","x-gitlab-feature-category":"source_code_management"};
  const url = `https://code.ornl.gov/api/graphql`

  const opts = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...headers,
    }
  };

  gl.startup_graphql_calls = gl.startup_graphql_calls.map(call => ({
    ...call,
    fetchCall: fetch(url, {
      ...opts,
      credentials: 'same-origin',
      body: JSON.stringify(call)
    })
  }))
}


//]]>
</script>

<link rel="prefetch" href="/assets/webpack/monaco.04aa8e15.chunk.js">

<link rel="stylesheet" href="/assets/application-61901f0326d988f31e7216b84669e4fa62cd86a0de409e286e83cd639cc996d4.css" />
<link rel="stylesheet" href="/assets/page_bundles/tree-49ae6a2f72af332906799a87b8b74e44ede65ce71f393346d0a1abb47656411a.css" /><link rel="stylesheet" href="/assets/page_bundles/projects-ef49918abcedc951ed001e2954b3004935dadcc67b6cf14868d935665f66073c.css" /><link rel="stylesheet" href="/assets/page_bundles/commit_description-1e2cba4dda3c7b30dd84924809020c569f1308dea51520fe1dd5d4ce31403195.css" /><link rel="stylesheet" href="/assets/page_bundles/work_items-22a76cdd1fe2ae5431b7ff603f86212acaf81b49c4a932f19e3b3222dc1881ee.css" /><link rel="stylesheet" href="/assets/page_bundles/notes_shared-30de79203a0836dddd3a4cf7364d63afb16a0f2deb0bbc654b00692872696739.css" />
<link rel="stylesheet" href="/assets/application_utilities-58bec0f2dc46133fc9e8548af9854688398e9d7263cc0fd95ec5739f2a069dec.css" />
<link rel="stylesheet" href="/assets/tailwind-5a00dff8ce8fc18c18a3c6b73b419c326b11e7dafe7cb551d38642da788f5e8f.css" />


<link rel="stylesheet" href="/assets/fonts-fae5d3f79948bd85f18b6513a025f863b19636e85b09a1492907eb4b1bb0557b.css" />
<link rel="stylesheet" href="/assets/highlight/themes/white-99cce4f4b362f6840d7134d4129668929fde49c4da11d6ebf17f99768adbd868.css" />


<link rel="preload" href="/assets/application_utilities-58bec0f2dc46133fc9e8548af9854688398e9d7263cc0fd95ec5739f2a069dec.css" as="style" type="text/css">
<link rel="preload" href="/assets/application-61901f0326d988f31e7216b84669e4fa62cd86a0de409e286e83cd639cc996d4.css" as="style" type="text/css">
<link rel="preload" href="/assets/highlight/themes/white-99cce4f4b362f6840d7134d4129668929fde49c4da11d6ebf17f99768adbd868.css" as="style" type="text/css">




<script src="/assets/webpack/runtime.5ad91b6f.bundle.js" defer="defer"></script>
<script src="/assets/webpack/main.a61010e6.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.groups.analytics.dashboards-pages.groups.harbor.repositories-pages.groups.iteration_ca-fae0f519.5b107e61.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.groups.new-pages.import.gitlab_projects.new-pages.import.manifest.new-pages.projects.n-44c6c18e.77d582f4.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.search.show-super_sidebar.3f577741.chunk.js" defer="defer"></script>
<script src="/assets/webpack/super_sidebar.07831d6d.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects-pages.projects.activity-pages.projects.alert_management.details-pages.project-68d77824.79456cb0.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.groups.packages-pages.groups.registry.repositories-pages.groups.security.policies.edit-429ebfda.823e1603.chunk.js" defer="defer"></script>
<script src="/assets/webpack/105.c82720fa.chunk.js" defer="defer"></script>
<script src="/assets/webpack/106.f0b1a739.chunk.js" defer="defer"></script>
<script src="/assets/webpack/127.d4e91245.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.show-pages.projects.snippets.show-pages.projects.tre-c684fcf6.03ac3868.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.edit-pages.projects.blob.new-pages.projects.blob.show-pages.projects.sho-ec79e51c.9677e14e.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.groups.show-pages.projects.blob.show-pages.projects.show-pages.projects.tree.show.dd816e95.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.security.vulnerabilities.show-pages.projects.show-pa-5ff3b950.5fc57aec.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.show-pages.projects.tree.show.4a86bbc9.chunk.js" defer="defer"></script>
<script src="/assets/webpack/commons-pages.projects.blob.show-pages.projects.tree.show-treeList.c6f35768.chunk.js" defer="defer"></script>
<script src="/assets/webpack/pages.projects.blob.show.70a24993.chunk.js" defer="defer"></script>

<meta content="object" property="og:type">
<meta content="GitLab" property="og:site_name">
<meta content="llvm/docs/RISCVUsage.rst · 3b75a5c4c84d17d6647ba079391722ed9be09f85 · llvm-doe / llvm-project · GitLab" property="og:title">
<meta content="ORNL/ITSD Gitlab Server" property="og:description">
<meta content="https://code.ornl.gov/assets/twitter_card-570ddb06edf56a2312253c5872489847a0f385112ddbcd71ccfa1570febab5d2.jpg" property="og:image">
<meta content="64" property="og:image:width">
<meta content="64" property="og:image:height">
<meta content="https://code.ornl.gov/llvm-doe/llvm-project/-/blob/3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm/docs/RISCVUsage.rst" property="og:url">
<meta content="summary" property="twitter:card">
<meta content="llvm/docs/RISCVUsage.rst · 3b75a5c4c84d17d6647ba079391722ed9be09f85 · llvm-doe / llvm-project · GitLab" property="twitter:title">
<meta content="ORNL/ITSD Gitlab Server" property="twitter:description">
<meta content="https://code.ornl.gov/assets/twitter_card-570ddb06edf56a2312253c5872489847a0f385112ddbcd71ccfa1570febab5d2.jpg" property="twitter:image">

<meta name="csrf-param" content="authenticity_token" />
<meta name="csrf-token" content="JlzwtyLjzKT-Sj44OEvo-2aa0xLZbnqkVDXSTggaeK35qHawBTeVNrK2FASsld9EigBUj-97aD1t33R7WpaIKg" />
<meta name="csp-nonce" />
<meta name="action-cable-url" content="/-/cable" />
<link href="/-/manifest.json" rel="manifest">
<link rel="icon" type="image/png" href="/uploads/-/system/appearance/favicon/1/22-G04365_BenjaminTaylor_Favicon_GreenLeafOnly_32x32_1mu.png" id="favicon" data-original-href="/uploads/-/system/appearance/favicon/1/22-G04365_BenjaminTaylor_Favicon_GreenLeafOnly_32x32_1mu.png" />
<link rel="apple-touch-icon" type="image/x-icon" href="/assets/apple-touch-icon-b049d4bc0dd9626f31db825d61880737befc7835982586d015bded10b4435460.png" />
<link href="/search/opensearch.xml" rel="search" title="Search GitLab" type="application/opensearchdescription+xml">




<meta content="ORNL/ITSD Gitlab Server" name="description">
<meta content="#ececef" name="theme-color">
</head>

<body class="tab-width-8 gl-browser-chrome gl-platform-mac" data-group="llvm-doe" data-group-full-path="llvm-doe" data-namespace-id="4015" data-page="projects:blob:show" data-page-type-id="3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm/docs/RISCVUsage.rst" data-project="llvm-project" data-project-full-path="llvm-doe/llvm-project" data-project-id="8748">

<script>
//<![CDATA[
gl = window.gl || {};
gl.client = {"isChrome":true,"isMac":true};


//]]>
</script>


<header class="header-logged-out" data-testid="navbar">
<a class="gl-sr-only gl-accessibility" href="#content-body">Skip to content</a>
<div class="container-fluid">
<nav aria-label="Explore GitLab" class="header-logged-out-nav gl-flex gl-gap-3 gl-justify-between">
<div class="gl-flex gl-items-center gl-gap-1">
<span class="gl-sr-only">GitLab</span>
<a title="Homepage" id="logo" class="header-logged-out-logo has-tooltip" aria-label="Homepage" href="/"><img class="brand-header-logo lazy" alt="" data-src="/uploads/-/system/appearance/header_logo/1/22-G04365_BenjaminTaylor_Favicon_WhiteLeafLarger_32x32_1mu.png" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" />
</a></div>
<ul class="gl-list-none gl-p-0 gl-m-0 gl-flex gl-gap-3 gl-items-center gl-grow">
<li class="header-logged-out-nav-item">
<a class="" href="/explore">Explore</a>
</li>
</ul>
<ul class="gl-list-none gl-p-0 gl-m-0 gl-flex gl-gap-3 gl-items-center gl-justify-end">
<li class="header-logged-out-nav-item">
<a href="/users/sign_in?redirect_to_referer=yes">Sign in</a>
</li>
</ul>
</nav>
</div>
</header>

<div class="layout-page page-with-super-sidebar">
<aside class="js-super-sidebar super-sidebar super-sidebar-loading" data-command-palette="{&quot;project_files_url&quot;:&quot;/llvm-doe/llvm-project/-/files/3b75a5c4c84d17d6647ba079391722ed9be09f85?format=json&quot;,&quot;project_blob_url&quot;:&quot;/llvm-doe/llvm-project/-/blob/3b75a5c4c84d17d6647ba079391722ed9be09f85&quot;}" data-force-desktop-expanded-sidebar="" data-is-saas="false" data-root-path="/" data-sidebar="{&quot;is_logged_in&quot;:false,&quot;context_switcher_links&quot;:[{&quot;title&quot;:&quot;Explore&quot;,&quot;link&quot;:&quot;/explore&quot;,&quot;icon&quot;:&quot;compass&quot;}],&quot;current_menu_items&quot;:[{&quot;id&quot;:&quot;project_overview&quot;,&quot;title&quot;:&quot;llvm-project&quot;,&quot;entity_id&quot;:8748,&quot;link&quot;:&quot;/llvm-doe/llvm-project&quot;,&quot;link_classes&quot;:&quot;shortcuts-project&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;manage_menu&quot;,&quot;title&quot;:&quot;Manage&quot;,&quot;icon&quot;:&quot;users&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/activity&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;activity&quot;,&quot;title&quot;:&quot;Activity&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/activity&quot;,&quot;link_classes&quot;:&quot;shortcuts-project-activity&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;members&quot;,&quot;title&quot;:&quot;Members&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/project_members&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;labels&quot;,&quot;title&quot;:&quot;Labels&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/labels&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;plan_menu&quot;,&quot;title&quot;:&quot;Plan&quot;,&quot;icon&quot;:&quot;planning&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/issues&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;project_issue_list&quot;,&quot;title&quot;:&quot;Issues&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/issues&quot;,&quot;pill_count_field&quot;:&quot;openIssuesCount&quot;,&quot;link_classes&quot;:&quot;shortcuts-issues has-sub-items&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;boards&quot;,&quot;title&quot;:&quot;Issue boards&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/boards&quot;,&quot;link_classes&quot;:&quot;shortcuts-issue-boards&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;milestones&quot;,&quot;title&quot;:&quot;Milestones&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/milestones&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;iterations&quot;,&quot;title&quot;:&quot;Iterations&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/cadences&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;project_wiki&quot;,&quot;title&quot;:&quot;Wiki&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/wikis/home&quot;,&quot;link_classes&quot;:&quot;shortcuts-wiki&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;code_menu&quot;,&quot;title&quot;:&quot;Code&quot;,&quot;icon&quot;:&quot;code&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/merge_requests&quot;,&quot;is_active&quot;:true,&quot;items&quot;:[{&quot;id&quot;:&quot;project_merge_request_list&quot;,&quot;title&quot;:&quot;Merge requests&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/merge_requests&quot;,&quot;pill_count_field&quot;:&quot;openMergeRequestsCount&quot;,&quot;link_classes&quot;:&quot;shortcuts-merge_requests&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;files&quot;,&quot;title&quot;:&quot;Repository&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/tree/3b75a5c4c84d17d6647ba079391722ed9be09f85&quot;,&quot;link_classes&quot;:&quot;shortcuts-tree&quot;,&quot;is_active&quot;:true},{&quot;id&quot;:&quot;branches&quot;,&quot;title&quot;:&quot;Branches&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/branches&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;commits&quot;,&quot;title&quot;:&quot;Commits&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/commits/3b75a5c4c84d17d6647ba079391722ed9be09f85&quot;,&quot;link_classes&quot;:&quot;shortcuts-commits&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;tags&quot;,&quot;title&quot;:&quot;Tags&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/tags&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;graphs&quot;,&quot;title&quot;:&quot;Repository graph&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/network/3b75a5c4c84d17d6647ba079391722ed9be09f85&quot;,&quot;link_classes&quot;:&quot;shortcuts-network&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;compare&quot;,&quot;title&quot;:&quot;Compare revisions&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/compare?from=doe\u0026to=3b75a5c4c84d17d6647ba079391722ed9be09f85&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;project_snippets&quot;,&quot;title&quot;:&quot;Snippets&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/snippets&quot;,&quot;link_classes&quot;:&quot;shortcuts-snippets&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;file_locks&quot;,&quot;title&quot;:&quot;Locked files&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/path_locks&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;build_menu&quot;,&quot;title&quot;:&quot;Build&quot;,&quot;icon&quot;:&quot;rocket&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/pipelines&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;pipelines&quot;,&quot;title&quot;:&quot;Pipelines&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/pipelines&quot;,&quot;link_classes&quot;:&quot;shortcuts-pipelines&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;jobs&quot;,&quot;title&quot;:&quot;Jobs&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/jobs&quot;,&quot;link_classes&quot;:&quot;shortcuts-builds&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;pipeline_schedules&quot;,&quot;title&quot;:&quot;Pipeline schedules&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/pipeline_schedules&quot;,&quot;link_classes&quot;:&quot;shortcuts-builds&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;artifacts&quot;,&quot;title&quot;:&quot;Artifacts&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/artifacts&quot;,&quot;link_classes&quot;:&quot;shortcuts-builds&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;deploy_menu&quot;,&quot;title&quot;:&quot;Deploy&quot;,&quot;icon&quot;:&quot;deployments&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/releases&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;releases&quot;,&quot;title&quot;:&quot;Releases&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/releases&quot;,&quot;link_classes&quot;:&quot;shortcuts-deployments-releases&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;packages_registry&quot;,&quot;title&quot;:&quot;Package Registry&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/packages&quot;,&quot;link_classes&quot;:&quot;shortcuts-container-registry&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;model_registry&quot;,&quot;title&quot;:&quot;Model registry&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/ml/models&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;operations_menu&quot;,&quot;title&quot;:&quot;Operate&quot;,&quot;icon&quot;:&quot;cloud-pod&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/environments&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;environments&quot;,&quot;title&quot;:&quot;Environments&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/environments&quot;,&quot;link_classes&quot;:&quot;shortcuts-environments&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;infrastructure_registry&quot;,&quot;title&quot;:&quot;Terraform modules&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/terraform_module_registry&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;monitor_menu&quot;,&quot;title&quot;:&quot;Monitor&quot;,&quot;icon&quot;:&quot;monitor&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/incidents&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;incidents&quot;,&quot;title&quot;:&quot;Incidents&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/incidents&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false},{&quot;id&quot;:&quot;analyze_menu&quot;,&quot;title&quot;:&quot;Analyze&quot;,&quot;icon&quot;:&quot;chart&quot;,&quot;avatar_shape&quot;:&quot;rect&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/value_stream_analytics&quot;,&quot;is_active&quot;:false,&quot;items&quot;:[{&quot;id&quot;:&quot;cycle_analytics&quot;,&quot;title&quot;:&quot;Value stream analytics&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/value_stream_analytics&quot;,&quot;link_classes&quot;:&quot;shortcuts-project-cycle-analytics&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;contributors&quot;,&quot;title&quot;:&quot;Contributor analytics&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/graphs/3b75a5c4c84d17d6647ba079391722ed9be09f85&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;ci_cd_analytics&quot;,&quot;title&quot;:&quot;CI/CD analytics&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/pipelines/charts&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;repository_analytics&quot;,&quot;title&quot;:&quot;Repository analytics&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/graphs/3b75a5c4c84d17d6647ba079391722ed9be09f85/charts&quot;,&quot;link_classes&quot;:&quot;shortcuts-repository-charts&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;code_review&quot;,&quot;title&quot;:&quot;Code review analytics&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/analytics/code_reviews&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;issues&quot;,&quot;title&quot;:&quot;Issue analytics&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/analytics/issues_analytics&quot;,&quot;is_active&quot;:false},{&quot;id&quot;:&quot;model_experiments&quot;,&quot;title&quot;:&quot;Model experiments&quot;,&quot;link&quot;:&quot;/llvm-doe/llvm-project/-/ml/experiments&quot;,&quot;is_active&quot;:false}],&quot;separated&quot;:false}],&quot;current_context_header&quot;:&quot;Project&quot;,&quot;support_path&quot;:&quot;https://about.gitlab.com/get-help/&quot;,&quot;docs_path&quot;:&quot;/help/docs&quot;,&quot;display_whats_new&quot;:false,&quot;show_version_check&quot;:null,&quot;search&quot;:{&quot;search_path&quot;:&quot;/search&quot;,&quot;issues_path&quot;:&quot;/dashboard/issues&quot;,&quot;mr_path&quot;:&quot;/dashboard/merge_requests&quot;,&quot;autocomplete_path&quot;:&quot;/search/autocomplete&quot;,&quot;settings_path&quot;:&quot;/search/settings&quot;,&quot;search_context&quot;:{&quot;group&quot;:{&quot;id&quot;:4015,&quot;name&quot;:&quot;llvm-doe&quot;,&quot;full_name&quot;:&quot;llvm-doe&quot;},&quot;group_metadata&quot;:{&quot;issues_path&quot;:&quot;/groups/llvm-doe/-/issues&quot;,&quot;mr_path&quot;:&quot;/groups/llvm-doe/-/merge_requests&quot;},&quot;project&quot;:{&quot;id&quot;:8748,&quot;name&quot;:&quot;llvm-project&quot;},&quot;project_metadata&quot;:{&quot;mr_path&quot;:&quot;/llvm-doe/llvm-project/-/merge_requests&quot;,&quot;issues_path&quot;:&quot;/llvm-doe/llvm-project/-/issues&quot;},&quot;code_search&quot;:true,&quot;ref&quot;:&quot;3b75a5c4c84d17d6647ba079391722ed9be09f85&quot;,&quot;scope&quot;:null,&quot;for_snippets&quot;:null}},&quot;panel_type&quot;:&quot;project&quot;,&quot;shortcut_links&quot;:[{&quot;title&quot;:&quot;Snippets&quot;,&quot;href&quot;:&quot;/explore/snippets&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-snippets&quot;},{&quot;title&quot;:&quot;Groups&quot;,&quot;href&quot;:&quot;/explore/groups&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-groups&quot;},{&quot;title&quot;:&quot;Projects&quot;,&quot;href&quot;:&quot;/explore/projects/starred&quot;,&quot;css_class&quot;:&quot;dashboard-shortcuts-projects&quot;}],&quot;terms&quot;:null}"></aside>

<div class="content-wrapper">
<div class="broadcast-wrapper">




</div>
<div class="alert-wrapper alert-wrapper-top-space gl-flex gl-flex-col gl-gap-3 container-fluid container-limited">






























</div>
<div class="top-bar-fixed container-fluid" data-testid="top-bar">
<div class="top-bar-container gl-flex gl-items-center gl-gap-2">
<div class="gl-grow gl-basis-0 gl-flex gl-items-center gl-justify-start gl-gap-3">
<button class="gl-button btn btn-icon btn-md btn-default btn-default-tertiary js-super-sidebar-toggle-expand super-sidebar-toggle -gl-ml-3" aria-controls="super-sidebar" aria-expanded="false" aria-label="Primary navigation sidebar" type="button"><svg class="s16 gl-icon gl-button-icon " data-testid="sidebar-icon"><use href="/assets/icons-aa2c8ddf99d22b77153ca2bb092a23889c12c597fc8b8de94b0f730eb53513f6.svg#sidebar"></use></svg>

</button>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"llvm-doe","item":"https://code.ornl.gov/llvm-doe"},{"@type":"ListItem","position":2,"name":"llvm-project","item":"https://code.ornl.gov/llvm-doe/llvm-project"},{"@type":"ListItem","position":3,"name":"Repository","item":"https://code.ornl.gov/llvm-doe/llvm-project/-/blob/3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm/docs/RISCVUsage.rst"}]}


</script>
<div data-testid="breadcrumb-links" id="js-vue-page-breadcrumbs-wrapper">
<div data-breadcrumbs-json="[{&quot;text&quot;:&quot;llvm-doe&quot;,&quot;href&quot;:&quot;/llvm-doe&quot;,&quot;avatarPath&quot;:null},{&quot;text&quot;:&quot;llvm-project&quot;,&quot;href&quot;:&quot;/llvm-doe/llvm-project&quot;,&quot;avatarPath&quot;:null},{&quot;text&quot;:&quot;Repository&quot;,&quot;href&quot;:&quot;/llvm-doe/llvm-project/-/blob/3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm/docs/RISCVUsage.rst&quot;,&quot;avatarPath&quot;:null}]" id="js-vue-page-breadcrumbs"></div>
<div id="js-injected-page-breadcrumbs"></div>
</div>


</div>
<div class="gl-flex-none gl-flex gl-items-center gl-justify-center">
<div id="js-advanced-search-modal"></div>

</div>
<div class="gl-grow gl-basis-0 gl-flex gl-items-center gl-justify-end">
<div id="js-work-item-feedback"></div>


</div>
</div>
</div>

<div class="container-fluid container-limited project-highlight-puc">
<main class="content" id="content-body" itemscope itemtype="http://schema.org/SoftwareSourceCode">
<div class="flash-container flash-container-page sticky" data-testid="flash-container">
<div id="js-global-alerts"></div>
</div>






<div class="js-signature-container" data-signatures-path="/llvm-doe/llvm-project/-/commits/c17a914675f8fcadbf0ef440aae7e0ab6c49ec0c/signatures?limit=1"></div>

<div class="tree-holder gl-pt-4" id="tree-holder">
<div class="nav-block">
<div class="tree-ref-container">
<div class="tree-ref-holder gl-max-w-26">
<div data-project-id="8748" data-project-root-path="/llvm-doe/llvm-project" data-ref="3b75a5c4c84d17d6647ba079391722ed9be09f85" data-ref-type="" id="js-tree-ref-switcher"></div>
</div>
<ul class="breadcrumb repo-breadcrumb">
<li class="breadcrumb-item">
<a href="/llvm-doe/llvm-project/-/tree/3b75a5c4c84d17d6647ba079391722ed9be09f85">llvm-project
</a></li>
<li class="breadcrumb-item">
<a href="/llvm-doe/llvm-project/-/tree/3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm">llvm</a>
</li>
<li class="breadcrumb-item">
<a href="/llvm-doe/llvm-project/-/tree/3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm/docs">docs</a>
</li>
<li class="breadcrumb-item">
<a href="/llvm-doe/llvm-project/-/blob/3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm/docs/RISCVUsage.rst"><strong>RISCVUsage.rst</strong>
</a></li>
</ul>
</div>
<div class="tree-controls gl-flex gl-flex-wrap sm:gl-flex-nowrap gl-items-baseline gl-gap-3">
<button class="gl-button btn btn-md btn-default has-tooltip shortcuts-find-file" title="Go to file, press &lt;kbd class=&#39;flat ml-1&#39; aria-hidden=true&gt;/~&lt;/kbd&gt; or &lt;kbd class=&#39;flat ml-1&#39; aria-hidden=true&gt;t&lt;/kbd&gt;" aria-keyshortcuts="/+~ t" data-html="true" data-event-tracking="click_find_file_button_on_repository_pages" type="button"><span class="gl-button-text">
Find file

</span>

</button>
<a data-event-tracking="click_blame_control_on_blob_page" class="gl-button btn btn-md btn-default js-blob-blame-link" href="/llvm-doe/llvm-project/-/blame/3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm/docs/RISCVUsage.rst"><span class="gl-button-text">
Blame
</span>

</a>
<a aria-keyshortcuts="y" class="gl-button btn btn-md btn-default has-tooltip js-data-file-blob-permalink-url" data-html="true" title="Go to permalink &lt;kbd class=&#39;flat ml-1&#39; aria-hidden=true&gt;y&lt;/kbd&gt;" href="/llvm-doe/llvm-project/-/blob/3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm/docs/RISCVUsage.rst"><span class="gl-button-text">
Permalink
</span>

</a>
</div>
</div>

<div class="info-well">
<div class="well-segment">
<ul class="blob-commit-info">
<li class="commit flex-row js-toggle-container" id="commit-c17a9146">
<div class="gl-self-start gl-block">
<a href="mailto:t_tttie@163.com"><img alt="T-Tie&#39;s avatar" src="https://secure.gravatar.com/avatar/32558a1fcb87ee424f849d1dc0577046c8ffe0a774373f53ee56c28b4eadce7e?s=64&amp;d=identicon" class="avatar s32 gl-inline-block" title="T-Tie"></a>
</div>
<div class="commit-detail flex-list gl-flex gl-justify-between gl-items-start gl-grow gl-min-w-0">
<div class="commit-content gl-self-center" data-testid="commit-content">
<div class="gl-flex sm:gl-hidden gl-gap-3 gl-items-center">
<div class="committer gl-text-sm">
<time class="js-timeago" title="Nov 8, 2024 7:01am" datetime="2024-11-08T07:01:51Z" tabindex="0" aria-label="Nov 8, 2024 7:01am" data-toggle="tooltip" data-placement="bottom" data-container="body">Nov 08, 2024</time>
</div>
<a class="gl-button btn btn-md btn-link commit-row-message js-onboarding-commit-item" href="/llvm-doe/llvm-project/-/commit/c17a914675f8fcadbf0ef440aae7e0ab6c49ec0c"><svg class="s16 gl-icon gl-button-icon " data-testid="commit-icon"><use href="/assets/icons-aa2c8ddf99d22b77153ca2bb092a23889c12c597fc8b8de94b0f730eb53513f6.svg#commit"></use></svg>
<span class="gl-button-text">
c17a9146

</span>

</a></div>
<div class="gl-hidden sm:gl-block">
<a class="commit-row-message item-title js-onboarding-commit-item " href="/llvm-doe/llvm-project/-/commit/c17a914675f8fcadbf0ef440aae7e0ab6c49ec0c">[RISCV] Add Smdbltrp and Ssdbltrp extension (#111837)</a>
<span class="commit-row-message d-inline d-sm-none">
&middot;
c17a9146
</span>
<button class="gl-button btn btn-icon btn-md btn-default button-ellipsis-horizontal js-toggle-button" data-toggle="tooltip" data-container="body" data-collapse-title="Toggle commit description" data-expand-title="Toggle commit description" title="Toggle commit description" aria-label="Toggle commit description" type="button"><svg class="s16 gl-icon gl-button-icon " data-testid="ellipsis_h-icon"><use href="/assets/icons-aa2c8ddf99d22b77153ca2bb092a23889c12c597fc8b8de94b0f730eb53513f6.svg#ellipsis_h"></use></svg>

</button>
<div class="committer gl-text-sm">
<a class="commit-author-link" href="mailto:t_tttie@163.com">T-Tie</a> authored <time class="js-timeago" title="Nov 8, 2024 7:01am" datetime="2024-11-08T07:01:51Z" tabindex="0" aria-label="Nov 8, 2024 7:01am" data-toggle="tooltip" data-placement="bottom" data-container="body">Nov 08, 2024</time>
</div>


<pre class="commit-row-description gl-whitespace-pre-wrap js-toggle-content">&#x000A;Smdbltrp and Ssdbltrp supports are added in this PR.&#x000A;Specification link(Smdbltrp) :&#x000A;[<a href="https://github.com/riscv/riscv-isa-manual/blob/main/src/smdbltrp.adoc%5D(url)" rel="nofollow noreferrer noopener" target="_blank">https://github.com/riscv/riscv-isa-manual/blob/main/src/smdbltrp.adoc](url)</a>&#x000A;Specification link(Ssdbltrp) :&#x000A;[<a href="https://github.com/riscv/riscv-isa-manual/blob/main/src/ssdbltrp.adoc%5D(url)" rel="nofollow noreferrer noopener" target="_blank">https://github.com/riscv/riscv-isa-manual/blob/main/src/ssdbltrp.adoc](url)</a></pre>
</div>
</div>
<div class="commit-actions gl-flex gl-items-center gl-gap-3">
<div class="gl-hidden sm:gl-flex gl-items-center gl-gap-3">
<a class="js-loading-signature-badge" data-commit-sha="c17a914675f8fcadbf0ef440aae7e0ab6c49ec0c" data-placement="top" data-title="GPG signature (loading...)" data-toggle="tooltip" role="button" tabindex="0"></a>

<div class="js-commit-pipeline-status" data-endpoint="/llvm-doe/llvm-project/-/commit/c17a914675f8fcadbf0ef440aae7e0ab6c49ec0c/pipelines?ref=3b75a5c4c84d17d6647ba079391722ed9be09f85"></div>
<div class="btn-group gl-hidden sm:gl-flex">
<span class="gl-button btn btn-label btn-md btn-default dark:!gl-bg-neutral-800" type="button"><span class="gl-button-text gl-font-monospace">
c17a9146

</span>

</span><button class="gl-button btn btn-icon btn-md btn-default " title="Copy commit SHA" aria-label="Copy commit SHA" aria-live="polite" data-toggle="tooltip" data-placement="bottom" data-container="body" data-html="true" data-category="primary" data-size="medium" data-clipboard-text="c17a914675f8fcadbf0ef440aae7e0ab6c49ec0c" type="button"><svg class="s16 gl-icon gl-button-icon " data-testid="copy-to-clipboard-icon"><use href="/assets/icons-aa2c8ddf99d22b77153ca2bb092a23889c12c597fc8b8de94b0f730eb53513f6.svg#copy-to-clipboard"></use></svg>

</button>

</div>
</div>
<div class="gl-block sm:gl-hidden">
<button class="gl-button btn btn-icon btn-md btn-default button-ellipsis-horizontal text-expander js-toggle-button" data-toggle="tooltip" data-container="body" data-collapse-title="Toggle commit description" data-expand-title="Toggle commit description" title="Toggle commit description" aria-label="Toggle commit description" type="button"><svg class="s16 gl-icon gl-button-icon " data-testid="ellipsis_h-icon"><use href="/assets/icons-aa2c8ddf99d22b77153ca2bb092a23889c12c597fc8b8de94b0f730eb53513f6.svg#ellipsis_h"></use></svg>

</button>
</div>
<div data-event-tracking="click_history_control_on_blob_page" data-history-link="/llvm-doe/llvm-project/-/commits/3b75a5c4c84d17d6647ba079391722ed9be09f85/llvm/docs/RISCVUsage.rst" id="js-commit-history-link"></div>
</div>
</div>
<div class="gl-block sm:gl-hidden">
<div class="gl-hidden js-toggle-content gl-mt-6">
<a class="commit-row-message item-title js-onboarding-commit-item " href="/llvm-doe/llvm-project/-/commit/c17a914675f8fcadbf0ef440aae7e0ab6c49ec0c">[RISCV] Add Smdbltrp and Ssdbltrp extension (#111837)</a>
<div class="committer gl-text-sm">
<a class="commit-author-link" href="mailto:t_tttie@163.com">T-Tie</a> authored <time class="js-timeago" title="Nov 8, 2024 7:01am" datetime="2024-11-08T07:01:51Z" tabindex="0" aria-label="Nov 8, 2024 7:01am" data-toggle="tooltip" data-placement="bottom" data-container="body">Nov 08, 2024</time>
</div>

<pre class="commit-row-description gl-whitespace-pre-wrap js-toggle-content">&#x000A;Smdbltrp and Ssdbltrp supports are added in this PR.&#x000A;Specification link(Smdbltrp) :&#x000A;[<a href="https://github.com/riscv/riscv-isa-manual/blob/main/src/smdbltrp.adoc%5D(url)" rel="nofollow noreferrer noopener" target="_blank">https://github.com/riscv/riscv-isa-manual/blob/main/src/smdbltrp.adoc](url)</a>&#x000A;Specification link(Ssdbltrp) :&#x000A;[<a href="https://github.com/riscv/riscv-isa-manual/blob/main/src/ssdbltrp.adoc%5D(url)" rel="nofollow noreferrer noopener" target="_blank">https://github.com/riscv/riscv-isa-manual/blob/main/src/ssdbltrp.adoc](url)</a></pre>
</div>
</div>
</li>

</ul>
</div>
<div class="gl-hidden sm:gl-block">
<div data-blob-path="llvm/docs/RISCVUsage.rst" data-branch="3b75a5c4c84d17d6647ba079391722ed9be09f85" data-branch-rules-path="/llvm-doe/llvm-project/-/settings/repository#js-branch-rules" data-project-path="llvm-doe/llvm-project" id="js-code-owners"></div>

</div>
</div>
<div class="blob-content-holder js-per-page" data-blame-per-page="1000" id="blob-content-holder">
<div data-blob-path="llvm/docs/RISCVUsage.rst" data-can-download-code="true" data-explain-code-available="false" data-new-workspace-path="/-/remote_development/workspaces/new" data-original-branch="3b75a5c4c84d17d6647ba079391722ed9be09f85" data-project-path="llvm-doe/llvm-project" data-ref-type="" data-resource-id="gid://gitlab/Project/8748" data-user-id="" id="js-view-blob-app">
<div class="gl-spinner-container" role="status"><span aria-hidden class="gl-spinner gl-spinner-md gl-spinner-dark !gl-align-text-bottom"></span><span class="gl-sr-only !gl-absolute">Loading</span>
</div>
</div>
</div>

</div>
<script>
//<![CDATA[
  window.gl = window.gl || {};
  window.gl.webIDEPath = '/-/ide/project/llvm-doe/llvm-project/edit/3b75a5c4c84d17d6647ba079391722ed9be09f85/-/llvm/docs/RISCVUsage.rst'


//]]>
</script>
<div data-ambiguous="false" data-ref="3b75a5c4c84d17d6647ba079391722ed9be09f85" id="js-ambiguous-ref-modal"></div>

</main>
</div>


</div>
</div>


<script>
//<![CDATA[
if ('loading' in HTMLImageElement.prototype) {
  document.querySelectorAll('img.lazy').forEach(img => {
    img.loading = 'lazy';
    let imgUrl = img.dataset.src;
    // Only adding width + height for avatars for now
    if (imgUrl.indexOf('/avatar/') > -1 && imgUrl.indexOf('?') === -1) {
      const targetWidth = img.getAttribute('width') || img.width;
      imgUrl += `?width=${targetWidth}`;
    }
    img.src = imgUrl;
    img.removeAttribute('data-src');
    img.classList.remove('lazy');
    img.classList.add('js-lazy-loaded');
    img.dataset.testid = 'js-lazy-loaded-content';
  });
}

//]]>
</script>
<script>
//<![CDATA[
gl = window.gl || {};
gl.experiments = {};


//]]>
</script>

</body>
</html>

