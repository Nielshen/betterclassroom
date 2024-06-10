
const getApiUrl = (logging = false) => {
    const prodUrl = import.meta.env.VITE_API_PROD_URL_RAW
    const localClusterUrl = import.meta.env.VITE_API_CLUSTER_URL_RAW
    const testUrl = import.meta.env.VITE_API_TEST_URL_RAW
    const hostname = window.location.hostname
    logging ? console.log(window.location.hostname) : null
    if (hostname === 'localhost' || hostname.startsWith("127.")) {
        return prodUrl // localhost:5000
    } else if (hostname === 'better-classrooom.com') {
        return localClusterUrl
    } else {
        return prodUrl //  betterclassroom-cluster.in.htwg-konstanz.de
    }

}


export {
    getApiUrl
}