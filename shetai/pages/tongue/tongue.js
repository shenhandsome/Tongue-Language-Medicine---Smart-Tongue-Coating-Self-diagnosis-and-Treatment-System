var app = getApp();
Page({
  data: {
    devicePosition: 'front', // 相机前后置
    authCamera: false, //用户是否运行授权拍照  
    flash: false, // 闪光灯
    upload_status: true, // 上传状态
    imagelist: [], //记录上传照片
    upload_dic: "", // 上传状态对应的描述
    uploadHidden: true, // 上传过程的加载界面
    imagecount: 0, // 记录已经上传了几张照片，
    mHidden: 0, // 拍照提示是否隐藏
    uploadHidden: true, //正在上传提示
    feature: [],
  },

  // 页面弹窗关闭
  closeModel: function () {
    var that = this
    that.setData({
      mHidden: true
    });
  },

  // 页面弹窗确定
  confirmModel: function () {
    var that = this
    that.setData({
      mHidden: true
    });
  },

  failfun: function () {
    app.globalData.mHidden = this.data.mHidden;
    app.globalData.imagecount = this.data.imagecount;
    wx.reLaunch({
      url: '/pages/tongue/tongue',
    });
  },

  // 用户拒绝使用相机时触发的事件
  handleCameraError: function () {
    authCamera: false;
    wx.showToast({
      title: '用户拒绝使用摄像头',
      icon: 'none'
    })
  },

  // 翻转相机前后置
  reverseCamera: function () {
    this.setData({
      devicePosition: "back" === this.data.devicePosition ? "front" : "back",
      mHidden: true
    });
  },

  //拍摄照片  
  takePhoto: function () {
    var that = this;
    wx.createCameraContext().takePhoto({
      quality: 'low', //拍摄质量(high:高质量 normal:普通质量 low:高质量)  
      success: (res) => {
        // 拍摄成功，显示正在上传，禁用相机
        that.setData({
          uploadHidden: false,
        })

        //上传图片到服务器后端
        var pic = res.tempImagePath;
        wx.uploadFile({
          url: 'http://127.0.0.1:8000/tongue',  
          filePath: String(pic),
          name: 'image',
          dataType:'JSON',  
          success: function (e) {
            // 关闭正在上传
            that.setData({
              uploadHidden: true,
            });
             // 解析接收到的数据
             var response_data = JSON.parse(e.data);
             if (response_data && response_data.answer && response_data.response_text) 
            {
             // 替换转义字符
                   var answer = response_data.answer.replace(/\\n/g, '\n');
                   var response_text = response_data.response_text.replace(/\\n/g, '\n');
                   // 跳转到指定页面，并传递数据
                   wx.navigateTo({
                     url: '/pages/tonguereport/tonguereport?answer=' + encodeURIComponent(answer) + '&response_text=' + encodeURIComponent(response_text)
                               });
                   } else {
                 // 如果没有接收到数据，提示用户重新拍照
                   wx.showToast({
                     title: '请重新拍照',
                     icon: 'none',
                     duration: 2000
                   });
                  }
          },
        })
      },
      fail: (res) => {
        that.setData({
          upload_status: false,
          upload_dic: "拍照失败，请重新拍照",
        })
      },
    })
  },

  // 相册选择图片
  chooseImage() {
    var that = this;
    wx.chooseImage({
      count: 1, // 最多选择多少张
      sizeType: ['compressed'], // 大小，是否原图
      sourceType: ['album'],
      success: function (res) {
        // 照片选择成功
        that.setData({
          uploadHidden: false, // 显示正在上传
        })
        //上传图片到服务器  
        var pic = res.tempFilePaths[0];
        console.log(pic)
        wx.uploadFile({
          url: 'http://127.0.0.1:8000/tongue',
          filePath: String(pic),
          name: 'image',
          dataType:'JSON',
          success: function (e) {
            // 关闭正在上传
            that.setData({
              uploadHidden: true,
            });
             // 解析接收到的数据
            var response_data = JSON.parse(e.data);
            // 如果接收到了数据
            if (response_data && response_data.answer && response_data.response_text) 
            {
            // 替换转义字符
                  var answer = response_data.answer.replace(/\\n/g, '\n');
                  var response_text = response_data.response_text.replace(/\\n/g, '\n');
                  // 跳转到指定页面，并传递数据
                  wx.navigateTo({
                    url: '/pages/tonguereport/tonguereport?answer=' + encodeURIComponent(answer) + '&response_text=' + encodeURIComponent(response_text)
                              });
                  } else {
                // 如果没有接收到数据，提示用户重新拍照
                  wx.showToast({
                    title: '请重新拍照',
                    icon: 'none',
                    duration: 2000
                  });
                 }
          },
        })
      },
      fail: (res) => {
        that.setData({
          // 选择图片失败
          upload_status: false,
          upload_dic: "选择图片失败，请重新选择或拍照",
        })
      },
    })
  },

  // 获取用户相机授权
  getCameraSetting() {
    const that = this
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.camera']) {
          // 用户已经授权
          that.setData({
            authCamera: true
          });
          wx.navigateBack({
            delta: 1,
          });
        } else {
          // 用户还没有授权，向用户发起授权请求
          wx.authorize({
            scope: 'scope.camera',
            success() { // 用户同意授权
              that.setData({
                authCamera: true
              });
              wx.navigateBack({
                delta: 1,
              });
            },
            fail() { // 用户不同意授权
              that.setData({
                authCamera: false
              });
              wx.navigateBack({
                delta: 1,
              });
              wx.showToast({
                title: '授权失败',
                icon: 'none',
                duration: 3000
              })
            }
          })
        }
      },
      fail: res => {
        console.log('获取用户授权信息失败')
        wx.showToast({
          title: '获取用户授权信息失败',
          icon: 'none',
          duration: 3000
        });
        that.setData({
          authCamera: false
        });
        wx.navigateBack({
          delta: 1,
        });
      }
    })
  },

  onLoad: function () {
    this.setData({
      imagelist: app.globalData.imagelist, // 保存用户拍的两张照片
      imagecount: app.globalData.imagecount,
      mHidden: app.globalData.mHidden, // 拍照提示是否隐藏
      feature: app.globalData.tonguefeature,
    })
    wx.getSetting({
      success: (res) => {
        if (res.authSetting["scope.camera"]) {
          this.setData({
            authCamera: true,
          })
        } else {
          this.setData({
            authCamera: false,
          })
        }
      }
    });
  },
})