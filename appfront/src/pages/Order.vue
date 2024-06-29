<!-- 
下单页面 /order/:id
-->

<template>
    <div class="OrderWindow">
      <div v-if="!confirm" class="confirm-windows">
        <div class="order-info">
          <img v-bind:src="item.image_url" class="item_img" alt="">
          <div class="item_details">
            <h3>{{item.title}}</h3>
            <div>
              <div class="item_list">
                <p style="color: #7a7a7a; margin-right: 10px;">活&nbsp;&nbsp;&nbsp;动:</p>
                <p>🛍最多送150元, 全店通用更划算🛍</p>
              </div>
              <div class="item_list">
                <p style="color: #7a7a7a; margin-right: 10px;">配&nbsp;&nbsp;&nbsp;送: </p>
                <p v-if="item.is_ship_free" style="margin-right: 10px;">48小时内发货 免运费</p>
                <p v-else style="margin-right: 10px;">48小时内发货 不包邮</p>
              </div>
              <div class="item_list">
                <p style="color: #7a7a7a; margin-right: 10px;">保&nbsp;&nbsp;&nbsp;障: </p>
                <p style="margin-right: 10px;">假一赔四 退货运费险 极速退款 7天无理由退换</p>
              </div>
            </div>
            <div class="item_list">
                <p style="color: #7a7a7a; margin-right: 10px;">价&nbsp;&nbsp;&nbsp;格: </p>
                <p style="margin-right: 10px; margin-top: 6px; color: red;">&yen;{{item.price}}</p>
              </div>
          </div>
        </div>

        <div style="margin-left: 60px; display: flex; flex-direction: column;">
          <h3 style="text-align: left; margin-bottom: 30px;">填写收货人信息</h3>
          <div style="display: flex; flex-direction: row;">
            <input type="text" class="name-input" placeholder="姓名" v-model="name"/>
            <input type="text" class="tel-input" placeholder="电话" v-model="tel"/>
          </div>
          <input type="text" class="address-input" placeholder="收货地址" v-model="address"/>
          <div style="display: flex; flex-direction: row; margin-top: 30px;">
            <el-button icon="el-icon-wallet" type="primary" @click='orderSend' :disabled="!isOK"
                :style="{opacity: isOK ? 1:0.5}"
                style="background-color: #FF7100;
                border-color: #e55e5e;
                width: 230px;">
                立即支付</el-button>
            <el-button icon="el-icon-close" type="primary" @click='returnEshop'
              style="background-color: #ffffff; color: #000000;
              border-color: #000000;
              width: 230px;">取消订单</el-button>
          </div>
        </div>
      </div>

      <div v-if="confirm" class="confirm-windows-ok">
        <h2>{{"支付成功！将在"+confirm_countdown+"s后返回商品库"}}</h2>
      </div>
    </div>
</template>

<script>
import axios from "axios";
import { getSingleGood ,createNewOrder } from "../api/api";
export default {
  name:'order',
  data() {
    return {
      confirm: false,
      item: 
      {
        'id': null,
        'title': '',
        'price': 0, 
        'image_url': null,
      },  // 商品
      name: '',
      tel: '',
      address: '',
      confirm_countdown: 3,
    };
  },
  computed:{
    //是否已经必填信息填写
    isOK(){
      if(this.name === '' | this.tel === '' | this.address === '')
        return false
      else
        return true
    }
  },
  methods: {
    returnEshop()
    {
      this.$router.push({ path: "/eshop" });
    },

    orderInit(good_id) {
      getSingleGood(good_id).then
      (response =>
        {
          if(response.status === 200) {
            this.item.title = response.data.name;
            this.item.price = response.data.price;
            this.item.image_url = response.data.front_image;
          }
        }
      ).catch
      (error =>
        {
          console.error('Enquery Failed.', error);
          this.$message.error('查询商品信息时发生网络错误，请检查网络状况！');
        }
      )
    },

    orderSend(){
      this.confirm = true;
      createNewOrder(this.item.id, this.address, this.name, this.tel).then
      (response =>
        {
          if(response.status === 201) {
            // for debug
            this.$message(`订单创建成功！`);
          }
        }
      ).catch
      (error =>
        {
          if(error.response) {
            if(error.response.status === 401) {
              console.error('Unauthorized.', error);
              // for debug
              this.$message.error('很抱歉，您暂未登录，无法创建订单！');
              return;
            }
          }
          console.error('Create New Order Failed.', error);
          this.$message.error('新建订单时发生网络错误，请检查网络状况！');
        }
      )
      //
      const intervalId = setInterval(() => {  
        if (this.confirm_countdown > 1) {  
          this.confirm_countdown--;  
        } else {  
          clearInterval(intervalId);   
          this.confirm_countdown = 3;
          this.$router.push({ path: "/eshop" });
        }  
      }, 1000);
    },
  },
  mounted() {

  },
  created() {
    // 获取当前商品的id
    const {id} = this.$route.params
    this.item.id = id

    // TODO 获取当前商品的部分信息用于填写订单
    this.orderInit(this.item.id);
    //
    // 为展示用，以下数据被写死
    // this.item.title = '辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染';
    // this.item.price = 49.99;
    // this.item.image_url = require('../assets/temp/1.jpg');

  }
}
</script>

<style scoped>
body {  
  background-color: #FFFEF5; /* 你想要的颜色 */  
}

.OrderWindow{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.confirm-windows{
  background-image: url("../assets/images/home/eshop/item_list.png");
  width: 958px;
  height: 530px;
}

.confirm-windows-ok{
  background-image: url("../assets/images/home/eshop/item_list.png");
  width: 958px;
  height: 530px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.order-info{
  display: flex;
  flex-direction: row;
  width: 850px;
  height: 250px;
  border-bottom: 1px solid #eeeeee;
  padding-bottom: 10px;
  margin-left: 60px;
}

.item_img{
  width: 190px;
  height: 190px;
  margin-top: 40px;
  margin-left: 0px;
}

.item_details{
  display: flex;
  margin-top: 20px;
  flex-direction: column;
  width: 600px;
  margin-left: 30px;
}

.item_details h3{
  text-align: left;
  margin-bottom: 0px
}

.item_details p{
  text-align: left;
  margin-bottom: 0px
}
.item_price{
  background-size: cover;
  width: 400px;
  height: 100px;
  margin-left: -5px;
  margin-top: -5px;
  margin-bottom: 10px;
}

.item_details p{
  margin-top: 8px;
  text-align: left;
  font-size: 14px;
  color: #7a7a7a;
}

.item_price h3{
  margin-left: 25px;
  margin-top: 55px;
  font-size: 25px;
  color: rgb(253, 59, 59);
}

.item_list{
  display: flex;
  flex-direction: row;
  margin-top: 10px;
}

.item_list p{
  font-size: 15px;
  color: black;
  margin-top: 5px;
}

.name-input {  
  border: none; 
  padding: 0; 
  border-bottom: 1px solid #ccc;  
  width: 150px; 
  color: #000000;  
  font-size: 16px;  
  line-height: 24px; 
  margin-right: 30px; 
}  
  
.name-input:focus {  
  outline: none; 
}

.tel-input {  
  border: none; 
  padding: 0; 
  border-bottom: 1px solid #ccc;  
  width: 300px; 
  color: #000000;  
  font-size: 16px;  
  line-height: 24px;  
}  

.tel-input:focus {  
  outline: none; 
}

.address-input {  
  border: none; 
  padding: 0; 
  border-bottom: 1px solid #ccc;  
  width: 480px; 
  color: #000000;  
  font-size: 16px;  
  line-height: 24px;  
  margin-top: 30px;
}  

.address-input:focus {  
  outline: none; 
}

</style>
