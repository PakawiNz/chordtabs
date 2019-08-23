module.exports = {
  publicPath: '/static/',
  devServer: {
    disableHostCheck: true,
    proxy: {
      '^/api': {
        target: 'http://localhost:8000',
      },
      '^/media': {
        target: 'http://localhost:8000',
      },
    }
  }
}
