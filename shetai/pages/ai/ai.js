Page({
  data: {
    backgroundurl:'/static/image/background1.png',
    question: '', // 用户输入的问题
    advice: '', // 中医建议
  },
  // 输入框内容变化时触发
  inputChange(event) {
    this.setData({
      question: event.detail.value // 更新用户输入的问题
    });
  },
  // 提交问题
  submitQuestion() {
    const that = this;
    wx.request({
      url: 'http://127.0.0.1:8000/ask', // Django后端
      method: 'GET',
      data: {
        question: this.data.question // 将用户输入的问题发送给后端
      },
      header:{  
        'content-type':'application/json'
     },
     dataType:'JSON',  
      success:function(res) {
        var advice = res.data.replace(/\\n/g, '\n'); 
        that.setData({
            advice:advice
        });
      },
      fail:function(err) {
        console.error('请求失败', err);
      }
    });
  },
});