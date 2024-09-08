pref("browser.search.defaultenginename", "Heexy");
pref("browser.search.defaultenginename", "Heexy");
//
/*
 * If you make changes to your about:config while the program is running, the
 * changes will be overwritten by the user.js when the application restarts.
 *
 * To make lasting changes to preferences, you will have to edit the user.js.
 */

/****************************************************************************
 * Betterfox                                                                *
 * "Ad meliora"                                                             *
 * version: 129                                                             *
 * url: https://github.com/yokoffing/Betterfox                              *
 * Betterfox by yokoffing, edited by Heexy
****************************************************************************/

/****************************************************************************
 * SECTION: FASTFOX                                                         *
****************************************************************************/
/** GENERAL ***/
//pref("content.notify.interval", 100000);
//
///** GFX ***/
//pref("gfx.canvas.accelerated.cache-items", 4096);
//pref("gfx.canvas.accelerated.cache-size", 512);
//pref("gfx.content.skia-font-cache-size", 20);
//
///** DISK CACHE ***/
//pref("browser.cache.jsbc_compression_level", 3);
//
///** MEDIA CACHE ***/
//pref("media.memory_cache_max_size", 65536);
//pref("media.cache_readahead_limit", 7200);
//pref("media.cache_resume_threshold", 3600);
//
///** IMAGE CACHE ***/
//pref("image.mem.decode_bytes_at_a_time", 32768);
//
///** NETWORK ***/
//pref("network.http.max-connections", 1800);
//pref("network.http.max-persistent-connections-per-server", 10);
//pref("network.http.max-urgent-start-excessive-connections-per-host", 5);
//pref("network.http.pacing.requests.enabled", false);
//pref("network.dnsCacheExpiration", 3600);
//pref("network.ssl_tokens_cache_capacity", 10240);
//
///** SPECULATIVE LOADING ***/
//pref("network.dns.disablePrefetch", true);
//pref("network.dns.disablePrefetchFromHTTPS", true);
//pref("network.prefetch-next", false);
//pref("network.predictor.enabled", false);
//pref("network.predictor.enable-prefetch", false);
//
///** EXPERIMENTAL ***/
//pref("layout.css.grid-template-masonry-value.enabled", true);
//pref("dom.enable_web_task_scheduling", true);
//pref("dom.security.sanitizer.enabled", true);

/****************************************************************************
 * SECTION: SECUREFOX                                                       *
****************************************************************************/
/** TRACKING PROTECTION ***/
pref("browser.contentblocking.category", "strict");
pref("urlclassifier.trackingSkipURLs", "*.reddit.com, *.twitter.com, *.twimg.com, *.tiktok.com");
pref("urlclassifier.features.socialtracking.skipURLs", "*.instagram.com, *.twitter.com, *.twimg.com");
pref("network.cookie.sameSite.noneRequiresSecure", true);
pref("browser.download.start_downloads_in_tmp_dir", true);
pref("browser.helperApps.deleteTempFileOnExit", true);
pref("browser.uitour.enabled", false);
pref("privacy.globalprivacycontrol.enabled", true);

/** OCSP & CERTS / HPKP ***/
pref("security.OCSP.enabled", 0);
pref("security.remote_settings.crlite_filters.enabled", true);
pref("security.pki.crlite_mode", 2);

/** SSL / TLS ***/
pref("security.ssl.treat_unsafe_negotiation_as_broken", true);
pref("browser.xul.error_pages.expert_bad_cert", true);
pref("security.tls.enable_0rtt_data", false);

/** DISK AVOIDANCE ***/
pref("browser.privatebrowsing.forceMediaMemoryCache", true);
pref("browser.sessionstore.interval", 60000);

/** SHUTDOWN & SANITIZING ***/
pref("privacy.history.custom", true);

/** SEARCH / URL BAR ***/
pref("browser.urlbar.trimHttps", true);
pref("browser.urlbar.untrimOnUserInteraction.featureGate", true);
pref("browser.search.separatePrivateDefault.ui.enabled", true);
pref("browser.urlbar.update2.engineAliasRefresh", true);
pref("browser.search.suggest.enabled", false);
pref("browser.urlbar.quicksuggest.enabled", false);
pref("browser.urlbar.suggest.quicksuggest.sponsored", false);
pref("browser.urlbar.suggest.quicksuggest.nonsponsored", false);
pref("browser.urlbar.groupLabels.enabled", false);
pref("browser.formfill.enable", false);
pref("security.insecure_connection_text.enabled", true);
pref("security.insecure_connection_text.pbmode.enabled", true);
pref("network.IDN_show_punycode", true);

/** HTTPS-FIRST POLICY ***/
pref("dom.security.https_first", true);

/** PASSWORDS ***/
pref("signon.formlessCapture.enabled", false);
pref("signon.privateBrowsingCapture.enabled", false);
pref("network.auth.subresource-http-auth-allow", 1);
pref("editor.truncate_user_pastes", false);

/** MIXED CONTENT + CROSS-SITE ***/
pref("security.mixed_content.block_display_content", true);
pref("pdfjs.enableScripting", false);
pref("extensions.postDownloadThirdPartyPrompt", false);

/** HEADERS / REFERERS ***/
pref("network.http.referer.XOriginTrimmingPolicy", 2);

/** CONTAINERS ***/
pref("privacy.userContext.ui.enabled", true);

/** WEBRTC ***/
pref("media.peerconnection.ice.proxy_only_if_behind_proxy", true);
pref("media.peerconnection.ice.default_address_only", true);

/** SAFE BROWSING ***/
pref("browser.safebrowsing.downloads.remote.enabled", false);

/** MOZILLA ***/
pref("permissions.default.desktop-notification", 2);
pref("permissions.default.geo", 2);
pref("permissions.manager.defaultsUrl", "");
pref("webchannel.allowObject.urlWhitelist", "");

/** TELEMETRY ***/
pref("datareporting.policy.dataSubmissionEnabled", false);
pref("datareporting.healthreport.uploadEnabled", false);
pref("toolkit.telemetry.unified", false);
pref("toolkit.telemetry.enabled", false);
pref("toolkit.telemetry.server", "data:,");
pref("toolkit.telemetry.archive.enabled", false);
pref("toolkit.telemetry.newProfilePing.enabled", false);
pref("toolkit.telemetry.shutdownPingSender.enabled", false);
pref("toolkit.telemetry.updatePing.enabled", false);
pref("toolkit.telemetry.bhrPing.enabled", false);
pref("toolkit.telemetry.firstShutdownPing.enabled", false);
pref("toolkit.telemetry.coverage.opt-out", true);
pref("toolkit.coverage.opt-out", true);
pref("toolkit.coverage.endpoint.base", "");
pref("browser.newtabpage.activity-stream.feeds.telemetry", false);
pref("browser.newtabpage.activity-stream.telemetry", false);

/** EXPERIMENTS ***/
pref("app.shield.optoutstudies.enabled", false);
pref("app.normandy.enabled", false);
pref("app.normandy.api_url", "");

/** CRASH REPORTS ***/
pref("breakpad.reportURL", "");
pref("browser.tabs.crashReporting.sendReport", false);
pref("browser.crashReports.unsubmittedCheck.autoSubmit2", false);

/** DETECTION ***/
pref("captivedetect.canonicalURL", "");
pref("network.captive-portal-service.enabled", false);
pref("network.connectivity-service.enabled", false);

/****************************************************************************
 * SECTION: PESKYFOX                                                        *
****************************************************************************/
/** MOZILLA UI ***/
pref("browser.privatebrowsing.vpnpromourl", "");
pref("extensions.getAddons.showPane", false);
pref("extensions.htmlaboutaddons.recommendations.enabled", false);
pref("browser.discovery.enabled", false);
pref("browser.shell.checkDefaultBrowser", false);
pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false);
pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", false);
pref("browser.preferences.moreFromMozilla", false);
pref("browser.aboutConfig.showWarning", false);
pref("browser.aboutwelcome.enabled", false);
pref("browser.tabs.tabmanager.enabled", false);
pref("browser.profiles.enabled", true);

/** THEME ADJUSTMENTS ***/
pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
pref("browser.compactmode.show", true);
pref("browser.display.focus_ring_on_anything", true);
pref("browser.display.focus_ring_style", 0);
pref("browser.display.focus_ring_width", 0);
pref("layout.css.prefers-color-scheme.content-override", 2);
pref("browser.privateWindowSeparation.enabled", false); // WINDOWS
pref("browser.newtabpage.activity-stream.newtabWallpapers.v2.enabled", true);

/** COOKIE BANNER HANDLING ***/
pref("cookiebanners.service.mode", 1);
pref("cookiebanners.service.mode.privateBrowsing", 1);

/** FULLSCREEN NOTICE ***/
pref("full-screen-api.transition-duration.enter", "0 0");
pref("full-screen-api.transition-duration.leave", "0 0");
pref("full-screen-api.warning.delay", -1);
pref("full-screen-api.warning.timeout", 0);

/** URL BAR ***/
pref("browser.urlbar.suggest.calculator", true);
pref("browser.urlbar.unitConversion.enabled", true);
pref("browser.urlbar.trending.featureGate", false);

/** NEW TAB PAGE ***/
pref("browser.newtabpage.activity-stream.feeds.topsites", false);
pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);

/** POCKET ***/
pref("extensions.pocket.enabled", false);

/** DOWNLOADS ***/
pref("browser.download.manager.addToRecentDocs", false);

/** PDF ***/
pref("browser.download.open_pdf_attachments_inline", true);

/** TAB BEHAVIOR ***/
pref("browser.bookmarks.openInTabClosesMenu", false);
pref("browser.menu.showViewImageInfo", true);
pref("findbar.highlightAll", true);
pref("layout.word_select.eat_space_to_next_word", false);

/** speed nyyyomth ***/
pref("content.notify.interval", 100000); // (.10s); default=120000 (.12s) - reflow interval - should be <= 0.1
pref("browser.cache.disk.enable", true); //should be default, disable if storage problems
pref("browser.cache.disk.max_entry_size", 91200); //increases max object size in disk cache to improve efficiency on spinny drives
pref("network.http.rcwn.enabled", false); //decrease network usage. !!WILL RENDER CACHE REALLY SLOW ON SPINNY DRIVES!!
pref("browser.cache.disk.metadata_memory_limit", 1000); // default=250 (0.25 MB); improves spinny drives efficiency
pref("browser.cache.disk.preload_chunk_count", 5); // DEFAULT 4 - make lower for lower ram usage
pref("browser.cache.disk.max_chunks_memory_usage", 50960); // DEFAULT 40 MB; lets more things get into cache, so more cache hits for big cache data
pref("browser.cache.disk.max_priority_chunks_memory_usage", 38000); // DEFAULT 40 MB; slightly decreased, so important cache files don't miss on spinny drives
pref("browser.cache.disk.free_space_soft_limit", 10240); // default=5120 (5 MB). ungarbles ur cache
pref("browser.cache.disk.free_space_hard_limit", 2048); // default=1024 (1 MB)
pref("browser.cache.jsbc_compression_level", 2); // makes cached js bytecode slightly compressed - helps with cache size
//pref("browser.cache.memory.capacity", -1); // DEFAULT; 256000=256 MB; 512000=500 MB; 1048576=1GB, 2097152=2GB
//pref("browser.cache.memory.max_entry_size", 10240); // (10 MB); default=5120 (5 MB)
pref("browser.sessionhistory.max_total_viewers", 5); // balances ram usage with session history(bach button) speed
pref("media.cache_size", 628000); // DEFAULT=512000; for some reason lowers ram usage, also huge speed improvement for SSDs
pref("media.memory_cache_max_size", 65536); // default=8192; AF=65536; alt=131072; ungarbles ur cache
pref("media.memory_caches_combined_limit_pc_sysmem", 5); // default=5;
pref("media.mediasource.enabled", true); // DEFAULT; this is here to prevent (built-in)plugins breaking videos
pref("media.cache_readahead_limit", 7200); // 120 min; default=60; stop reading ahead when our buffered data is this many seconds ahead of the current playback - increases ram usage, but makes unstable networks usable
pref("media.cache_resume_threshold", 3600); // 60 min; default=30; when a network connection is suspended, don't resume it until the amount of buffered data falls below this threshold
pref("image.mem.decode_bytes_at_a_time", 32768); // default=16384; alt=65536; chunk size for calls to the image decoders
pref("network.buffer.cache.count", 128); // default=24; increases the maximum number of cache entries for packets
pref("network.http.max-connections", 1800); // default=900
pref("network.http.max-persistent-connections-per-server", 10); // default=6; download connections; anything above 10 is excessive for the average user
pref("network.http.max-urgent-start-excessive-connections-per-host", 5); // default=3
//pref("network.http.pacing.requests.enabled", false); UNCOMMENT WHEN BROWSER RUNS SMOOTHLY ON THE LOWEST OF LOWEST DEVICES
pref("network.dnsCacheEntries", 1100); // default=400; can make dns resolving faster
pref("network.dnsCacheExpiration", 7200); // keep entries for 2 hours
pref("network.dnsCacheExpirationGracePeriod", 240); // default=60; cache DNS entries for 4 minutes after they expire
pref("network.ssl_tokens_cache_capacity", 10240); // default=2048; more TLS token caching (fast reconnects)
pref("network.dns.disablePrefetch", true);
    pref("network.dns.disablePrefetchFromHTTPS", false); // [FF127+ false]
pref("browser.low_commit_space_threshold_mb", 3276); // default=200; ONLY WINDOWS AND MACOS
pref("dom.ipc.processPrelaunch.fission.number", 2); // default=3; Process Preallocation Cache
pref("fission.webContentIsolationStrategy", 2);
pref("browser.preferences.defaultPerformanceSettings.enabled", false);
    pref("dom.ipc.processCount.webIsolated", 1); // one process per site origin (high value)
    pref("dom.ipc.processCount", 8); // determine by number of CPU cores/processors

/****************************************************************************
 * START: MY OVERRIDES                                                      *
****************************************************************************/
// visit https://github.com/yokoffing/Betterfox/wiki/Common-Overrides
// visit https://github.com/yokoffing/Betterfox/wiki/Optional-Hardening
// Enter your personal overrides below this line:

/****************************************************************************
 * SECTION: SMOOTHFOX                                                       *
****************************************************************************/
// visit https://github.com/yokoffing/Betterfox/blob/main/Smoothfox.js
// Enter your scrolling overrides below this line:
pref("apz.overscroll.enabled", true);
pref("general.smoothScroll", true);
pref("general.smoothScroll.msdPhysics.enabled", true);
pref("mousewheel.default.delta_multiplier_y", 280);

/****************************************************************************
 * END: BETTERFOX                                                           *
****************************************************************************/

// pref("browser.urlbar.update2.engineAliasRefresh"