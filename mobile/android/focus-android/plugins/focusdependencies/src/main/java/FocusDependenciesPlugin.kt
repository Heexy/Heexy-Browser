/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

import org.gradle.api.Plugin
import org.gradle.api.initialization.Settings

// If you ever need to force a toolchain rebuild (taskcluster) then edit the following comment.
// FORCE REBUILD 2023-05-05

class FocusDependenciesPlugin : Plugin<Settings> {
    override fun apply(settings: Settings) = Unit
}

object FocusVersions {
    object Adjust {
        const val adjust = "4.38.2"
        const val install_referrer = "2.2"
    }

    object AndroidX {
        const val constraint_layout_compose = "1.0.1"
        const val splashscreen = "1.0.1"
    }

    object Testing {
        const val falcon = "2.2.0"
        const val fastlane = "2.1.1"
        const val junit = "5.10.2"
    }
}

object FocusDependencies {
    const val androidx_constraint_layout_compose =
        "androidx.constraintlayout:constraintlayout-compose:${FocusVersions.AndroidX.constraint_layout_compose}"

    const val androidx_splashscreen = "androidx.core:core-splashscreen:${FocusVersions.AndroidX.splashscreen}"

    const val adjust = "com.adjust.sdk:adjust-android:${FocusVersions.Adjust.adjust}"
    const val install_referrer = "com.android.installreferrer:installreferrer:${FocusVersions.Adjust.install_referrer}"

    const val falcon = "com.jraska:falcon:${FocusVersions.Testing.falcon}"
    const val fastlane = "tools.fastlane:screengrab:${FocusVersions.Testing.fastlane}"

    const val testing_junit_api = "org.junit.jupiter:junit-jupiter-api:${FocusVersions.Testing.junit}"
    const val testing_junit_engine = "org.junit.jupiter:junit-jupiter-engine:${FocusVersions.Testing.junit}"
    const val testing_junit_params = "org.junit.jupiter:junit-jupiter-params:${FocusVersions.Testing.junit}"
}
