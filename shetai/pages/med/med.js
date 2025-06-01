Page({
  data: {
    backgroundurl:'/static/image/background2.png',
    medname: '', // 用户输入的药品名
    information: '', // 药品信息
  },
  // 输入框内容变化时触发
  inputChange(event) {
    this.setData({
      medname: event.detail.value // 更新用户输入的问题
    });
  },
  // 提交问题
  submitQuestion() {
    const that = this;
    wx.request({
      url: 'http://127.0.0.1:8000/med', // Django后端
      method: 'GET',
      data: {
        medname: this.data.medname // 将用户输入的问题发送给后端
      },
      header:{  
        'content-type':'application/json'
     },
     dataType:'JSON',  
      success:function(res) {
        var information = res.data.replace(/\\n/g, '\n'); 
        that.setData({
          information:information
        });
      },
      fail:function(err) {
        console.error('请求失败', err);
      }
    });
  },
});