<!-- 
订单评价 /ordercomment/:id
待完善功能：
    1. create() 获取待评价订单的基本信息
    2. sendcomment() 新建一条评论然后发送给后端
-->

<template>
    <div class="Ordercomment-Window">
      <div v-if="!confirm" class="details-windows">
        <el-input class="comment-input" autosize type="textarea" placeholder="展开说说对商品的想法吧..." 
            v-model="text" maxlength="110" show-word-limit></el-input>
        <div class="starsAndsend">
            <div style="display: flex; flex-direction: row; margin-bottom: 20px; border-bottom: 1px solid #eeeeee; padding-bottom: 10px;">
                <img v-bind:src="order.good.front_image" class="order_box" alt="">
                <div class="order-details">
                    <h5 v-html="order.good.name" class="ordername"></h5> 
                    <p>订单号: {{ order.id }}</p>
                    <p>下单时间: {{ order.good.create_time.slice(0, 10)+ ' '+ order.good.create_time.slice(11, 19) }}</p>
                </div>
            </div>
            <h3>您对商品满意吗？</h3> 
            <div style="margin-left: 90px;">
                <div style="display: flex; flex-direction: row; justify-content: left;">
                    <h5 style="margin-top: 0px; margin-right: 15px;">描述相符</h5>
                    <el-rate v-model="rate1" show-text :colors="colors"></el-rate>
                </div>
                <div style="display: flex; flex-direction: row; justify-content: left;">
                    <h5 style="margin-top: 0px; margin-right: 15px;">使用体验</h5>
                    <el-rate v-model="rate2" show-text :colors="colors"></el-rate>
                </div>
                <div style="display: flex; flex-direction: row; justify-content: left;">
                    <h5 style="margin-top: 0px; margin-right: 15px;">物流服务</h5>
                    <el-rate v-model="rate3" show-text :colors="colors"></el-rate>
                </div>
                <div style="display: flex; flex-direction: row; justify-content: left;">
                    <h5 style="margin-top: 0px; margin-right: 15px;">总体评价</h5>
                    <el-rate v-model="total" disabled show-text :colors="colors"></el-rate>
                </div>
            </div>
            <div style="display: flex; justify-content: flex-end;">
            <el-button :disabled="total==0 || total==null" icon="el-icon-s-promotion" type="primary" @click='sendComment'
                    style="background-color: #E55E5E; color: #ffffff;
                    border-color: #E55E5E;
                    width: 120px; height: 40px; margin-top: 30px; margin-right: 15px;"
                    :style="{opacity: total !== 0 &&total !== null ? 1 : 0.5}">发布</el-button>
            </div>
        </div> 
      </div>

      <div v-if="confirm" class="confirm-windows-ok">
        <h2>{{"评价成功！将在"+confirm_countdown+"s后返回我的订单"}}</h2>
      </div>
    </div>
</template>

<script>
import axios from "axios";
import { getSingleOrder, createNewGoodComment } from "../api/api";
export default {
  name:'ordercomment',
  data() {
    return {
      text: '',
      order_id: '',
      order: {},
      
      // 发布评论后页面变化+倒计时
      confirm: false,
      confirm_countdown: 3,

      // 评分变量
      rate1: null,
      rate2: null,
      rate3: null,
      colors: ['#99A9BF', '#F7BA2A', '#FF9900']
  }
  },
  computed:{
    total() {  
      if (this.rate1 !== null && this.rate2 !== null && this.rate3 !== null &&
          this.rate1 != 0 && this.rate2 != 0 && this.rate3 != 0) {  
        const sum = this.rate1 + this.rate2 + this.rate3;  
        return Math.floor(sum / 3);  
      }  
      return null;  
    }  
  },
  methods: {
    obtainOrderDetails()
    {
      getSingleOrder(this.order_id).then
      (response =>
        {
          if(response.status === 200) {
            // for debug
            this.$message.success(`成功查询到订单详情`);
            this.order = response.data;
          }
        }
      ).catch
      (error => 
        {
          console.error('Enquiry Failed.', error);
          this.$message.error('查询评论详情时发生网络错误，请检查网络状况！');
        }
      )

    },

    sendComment()
    {   
        this.confirm = true
        createNewGoodComment(this.order_id, this.total, this.text).then
        (response =>
          {
            if(response.status === 201) {
              // for debug
              this.$message.success(`成功评论！`);
            }
          }
        ).catch
        (error =>
          {

          }
        )
        //
        const intervalId = setInterval(() => {  
        if (this.confirm_countdown > 1) {  
          this.confirm_countdown--;  
        } else {  
          clearInterval(intervalId);   
          this.confirm_countdown = 3;
          this.$router.push({ path: "/myorder" });
        }  
      }, 1000);
    }
  },
  mounted() {

  },
  created() {
    const {id} = this.$route.params;
    this.order_id = id;

    this.obtainOrderDetails();
    // 测试用数据
    // this.order = {
    //     "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    //     "user": null,
    //     "good": 
    //     {
    //         "id": 17,
    //         "category": 
    //         {
    //             "name": "",
    //             "description": "",
    //             "category_type": 1
    //         },
    //         "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林",
    //         "brief_content": "",
    //         "content": "",
    //         "front_image": require('../assets/temp/1.jpg'),
    //         "price": 59.99,
    //         "create_time": "2024-06-11T06:23:17.284Z",
    //         "modify_time": "2024-06-11T06:23:17.284Z",
    //         "sold_num": 19,
    //         "click_num": 198,
    //         "comment_num": 10,
    //         "favor_num": 721,
    //         "is_new": false,
    //         "is_hot": false,
    //         "is_ship_free": true
    //     },
    //     "order_amount": 0,
    //     "is_sign": false,
    //     "address": "新日暮里祥和路0721号",
    //     "signer_name": "马牛逼",
    //     "signer_mobile": "19975765899",
    //     "create_time": "2024-06-19T06:26:17.284Z",
    //     "sign_time": "2024-06-19T06:26:17.284Z",
    // };
  }
}
</script>

<style scoped>
body {  
  background-color: #FFFEF5; /* 你想要的颜色 */  
}

.Ordercomment-Window{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.details-windows{
  background-image: url("../assets/images/home/eshop/item_list.png");
  width: 958px;
  height: 530px;
  display: flex;
  flex-direction: row;
  justify-content: left;
}

.comment-input{
    width: 500px;
    height: 460px;
    border: 1px solid #eeeeee;
    padding-bottom: 10px;
    font-size: 16px;
    margin-left: 25px;
    margin-top: 25px;
}

.details-windows>>>.el-textarea__inner {
    border: 0;
    resize: none;
}

.starsAndsend{  
  margin-left: 15px;
  display: flex;
  flex-direction: column;
  margin-top: 30px;
}

.order_box{
  width: 130px;
  height: 130px;
  margin-bottom: 10px;
  margin-left: 0px;
}

.order-details{
  display: flex; 
  flex-direction: column; 
  margin-left: 10px;
  width: 260px;
  text-align: left;
}

.order-details h5{
  height: 45px;
  font-size: 15px;
  margin-top: 0px;
  margin-bottom: 20px;
}

.order-details p{
  font-size: 14px;
  margin-top: 0px;
  margin-bottom: 5px;
}

.confirm-windows-ok{
  background-image: url("../assets/images/home/eshop/item_list.png");
  width: 958px;
  height: 530px;
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
