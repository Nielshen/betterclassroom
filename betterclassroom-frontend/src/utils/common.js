
const getApiUrl = (logging = false) => {
    const prodUrl = import.meta.env.VITE_API_PROD_URL_RAW
    const stagingUrl = import.meta.env.VITE_API_STAGING_URL_RAW
    const localClusterUrl = import.meta.env.VITE_API_CLUSTER_URL_RAW
    const testUrl = import.meta.env.VITE_API_TEST_URL_RAW
    return prodUrl
    const hostname = window.location.hostname
    logging ? console.log({ prodUrl, testUrl, hostname}) : null
    if (hostname === 'localhost' || hostname.startsWith("127.")) {
        return testUrl // localhost:5000
    } else if (hostname === 'better-classroom.com') {
        return localClusterUrl
    } else if (hostname === 'betterclassroom-staging.in.htwg-konstanz.de') {
        return stagingUrl
    } else {
        return prodUrl //  betterclassroom.in.htwg-konstanz.de
    }

}


export {
    getApiUrl
}