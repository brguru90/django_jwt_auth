const {createProxyMiddleware} = require("http-proxy-middleware")
// const streamify = require('stream-array');
const http = require("http")
var keepAliveAgent = new http.Agent({keepAlive: true})
module.exports = function (app) {
    app.use(
        "/api",
        createProxyMiddleware({
            target: "http://localhost:8000",
            changeOrigin: true,
            agent: keepAliveAgent,
            // ws: true,
            xfwd: true,
            pathRewrite: {
                "^/api": "/",
            },
        })
    )
}