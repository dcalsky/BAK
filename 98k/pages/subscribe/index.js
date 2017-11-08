// pages/subscribe/index.js

Page({
  onLoad: function () {
    wx.request({
      url: 'http://localhost:5000/sites',
      success: res => {
        const obj = res.data.sites.map(site => {return {
          val: site,
          content: site
        }})
        this.setData({
          siteRange: obj
        })
        this.fetch_post(res.data.sites[0])
      }
    })
  },
  /**
   * 页面的初始数据
   */
  data: {
    siteRange: [],
    siteIndex: 0,
    posts: []
  },
  fetch_post(siteVal) {
    wx.request({
      url: 'http://localhost:5000/posts',
      data: {
        site: siteVal
      },
      header: {
        'content-type': 'application/json'
      },
      success: (res) => {
        console.log(res.data)
        this.setData({
          posts: res.data.posts
        })
      }
    })
  },
  bindPickerChange: function (e) {
    const siteVal = this.data.siteRange[e.detail.value].val
    this.setData({
      siteIndex: e.detail.value
    })
    this.fetch_post(siteVal)
  }
})