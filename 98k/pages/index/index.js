//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    email: "",
    checkboxItems: [
      { name: '机械学院', value: '同济大学机械学院', checked: true },
      { name: '软件学院', value: '同济大学软件学院' },
      { name: '土木学院', value: '同济大学土木学院' },
      { name: '同济大学官网', value: '同济大学官网' }
    ],
  },
  bindKeyInput: function (e) {
    this.setData({
      email: e.detail.value
    })
  },
  submit: function(e) {
    const latestOne = this.data.checkboxItems.some(function(item) {
      return item.checked
    })
    if (!latestOne || this.data.email == '') {
      wx.showToast({
        title: '信息不完整',
        duration: 1500
      })
      return;
    }
    const sites = this.data.checkboxItems
      .filter(site => site.checked)
      .map(site => site.value)
    wx.request({
      url: 'http://localhost:5000/subscribe',
      method: 'POST',
      data: {
        email: this.data.email,
        sites: sites
      },
      success: (res) => {
        if (res.data.msg === 'ok') {
          wx.showToast({
            title: '订阅成功!',
            duration: 1500
          })
        }
      }
    })
  },
  checkboxChange: function (e) {
    var checkboxItems = this.data.checkboxItems, values = e.detail.value;
    for (var i = 0, lenI = checkboxItems.length; i < lenI; ++i) {
      checkboxItems[i].checked = false;

      for (var j = 0, lenJ = values.length; j < lenJ; ++j) {
        if (checkboxItems[i].value == values[j]) {
          checkboxItems[i].checked = true;
          break;
        }
      }
    }

    this.setData({
      checkboxItems: checkboxItems
    });
    console.log(checkboxItems)
  },

})
