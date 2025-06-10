#!/bin/bash
set -e -u -o pipefail

download_apk() {
    local app_id=$1

    # https://github.com/EFForg/apkeep/blob/master/src/apkpure.rs#L18C54-L18C61
    curl -sS "https://api.pureapk.com/m/v3/cms/app_version?hl=en-US&package_name=$app_id" \
        -H 'x-sv: 29' \
        -H 'x-abis: arm64-v8a,armeabi-v7a,armeabi' \
        -H 'x-gp: 1' |
        strings |
        grep "/APK" | # Download latest version in APK format
        head -n1 |
        xargs -rt curl -L -D >(grep -i "^content-disposition:") -o "$app_id.apk"
}

download_apk "$@"