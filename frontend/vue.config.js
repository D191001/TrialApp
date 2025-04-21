module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  },
  chainWebpack: config => {
    config.optimization.splitChunks({
      chunks: 'all',
      minSize: 20000,
      maxSize: 244000
    })
  },
  productionSourceMap: false,
  publicPath: '/',
  outputDir: 'dist'
}
