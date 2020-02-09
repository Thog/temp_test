const https = require("https")
const fs = require("fs")
const process = require("process")

const release = JSON.parse(fs.readFileSync(process.env['GITHUB_EVENT_PATH'])).release

var result = {
    version: release.name,
    artefacts: []
}

release.assets.forEach(asset => {
    const assetName = asset.name
    if (assetName.indexOf("ryujinx") == 0) {
        const assetSplit = assetName.split('-')[2].split('_')
        const url = asset.browser_download_url
        result.artefacts.push({
            "os": assetSplit[0],
            "arch": assetSplit[1].split('.')[0],
            'url': url
        })
    }

});

fs.writeFileSync(release.name + ".json", JSON.stringify(result, null, 2))


console.log(result)
