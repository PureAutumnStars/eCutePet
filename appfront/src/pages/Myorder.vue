<!-- 
我的订单 /myorder
-->

<template>
    <div class="OrderWindow">
        <div class="orders-windows">
            <ul v-for="(item,index) in paginatedOrders" :key="index" style="list-style-type: none; margin-top: 20px;">
              <li class="orderitem">
                  <img v-bind:src="item.good.front_image" class="order_box" alt="">
                  <div class="order-details">
                    <h5 v-html="item.good.name" class="ordername"></h5> 
                    <p> 订单号: {{ item.id }}</p>
                    <p> 收货信息: {{item.signer_name}},{{item.signer_mobile}},{{item.address}}</p>
                    <p> 下单时间: {{ item.good.create_time.slice(0, 10)+ ' '+ item.good.create_time.slice(11, 19) }}</p>
                    <p> 实付款: &yen;{{ item.good.price }}</p>
                  </div>
                  <div style="display: flex; flex-direction: row; width: 400px; justify-content: end; align-items: flex-end;">
                    <el-button icon="el-icon-check" type="primary" @click='confirmOrder(item)' :disabled="item.is_sign"
                        style="background-color: #ffffff; color: #000000;
                        border-color: #000000;
                        width: 120px; height: 40px;"
                        :style="{opacity: item.is_sign ? 0.5 : 1}">
                        {{item.is_sign ? '已收货' : '确认收货'}}</el-button>

                    <el-button icon="el-icon-chat-line-round" type="primary" :disabled="!item.is_sign" @click='makeComment(item)'
                    style="background-color: #ffffff; color: #000000;
                    border-color: #000000;
                    width: 120px; height: 40px; margin-right: 10px;"
                    :style="{opacity: item.is_sign ? 1 : 0.5}">评价</el-button>

                    <el-badge value="下单立抢现金券">
                    <el-button icon="el-icon-shopping-cart-2" type="primary" @click='routeTwice(item)'
                    style="background-color: #FF7100; color: #ffffff;
                    border-color: #FF7100;
                    width: 120px; height: 40px;">再买一单</el-button>
                    </el-badge>
                    
                  </div>
              </li>
            </ul>
        </div>
        <div style="margin-top: -65px; margin-bottom: 30px;">  
          <el-pagination  
            @size-change="handleSizeChange"  
            @current-change="handleCurrentChange"  
            :current-page="currentPage"  
            :page-sizes="[8]"  
            :page-size="pageSize"  
            layout="total, sizes, prev, pager, next, jumper"  
            :total="totalOrders">  
          </el-pagination>  
          </div>
    </div>
</template>

<script>
import axios from "axios";
import { getGoodCommentList, getOrdersList, getSingleOrder, reviseOrder } from "../api/api";
export default {
  name:'myorder',
  data() {
    return {
      myOrders: [],

      // 当前页面， 每页大小（固定，用于请求时做参数）以及订单数量
      currentPage: 1, 
      pageSize: 8, 
      totalOrders: 0, 
      
      // 评论启用按钮
      commented: false,
    };
  },
  computed: {  
    // 计算订单切片分页，可忽略
    paginatedOrders() {  
      const start = (this.currentPage - 1) * this.pageSize;  
      const end = start + this.pageSize;  
      return this.myOrders.slice(start, end);  
    },  
  },
  methods: {
    // 处理页面大小和页码的函数，可忽略
    handleSizeChange(val) {  
      this.pageSize = val;  
    },  
    handleCurrentChange(val) {  
      this.currentPage = val;  
    },

    myOrderInit() {
      getOrdersList('', '', 'create_time', 1, 199).then
      (response =>
        {
          if(response.status === 200) {
            this.totalOrders = response.data.count;
            this.myOrders = response.data.results;
            // for debug
            this.$message.success(`成功获取到您的订单列表！`);
          }
        }
      ).catch
      (error =>
        {
          if(error.response) {
            if(error.response.status === 401) {
              console.error('Unauthorized.', error);
              // for debug
              this.$message.error('很抱歉，您暂未登录，无法查看自己的订单列表！');
              return;
            }
          }
          console.error('Enquiry Failed.', error);
          this.$message.error('查询您的订单列表时发生网络错误，请检查网络状况！');
        }
      )
    },

    routeTwice(item){
        this.$router.push({name: 'item', params:{id: item.good.id}});
    },
    makeComment(item){
        this.$router.push({name: 'ordercomment', params:{id: item.id}});
    },
    confirmOrder(item){
        item.is_sign = true;
        this.$message
        ({
            message: `订单签收成功!`,
            type: 'success'
        });
        reviseOrder(
          item.id, 
          true, 
          item.address,
          item.signer_name,
          item.signer_mobile).then
        (response =>
          {
            if(response.status === 200) {
              // for debug
              // this.$message.success('已经成功修改订单签收状态！');
            }
          }
        ).catch
        (error =>
          {
            if(error.response) {
              if(error.response.status === 401) {
                console.error('Unauthorized.', error);
                // for debug
                this.$message.error('很抱歉，您暂未登录，无法查看自己的订单详情！');
                return;
              }
            }
            console.error('Enquiry Failed.', error);
            this.$message.error('修改订单状态时发生网络错误，请检查网络状况！');
          }
        )
    },
    routeDetails(item){
      this.$router.push({name: 'ordercomment', params:{id: item.id}});
    },
  },
  mounted() {

  },
  created() {
    this.myOrderInit();

    // this.totalOrders = 10;
    // this.myOrders = [
    //     {
    //     "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    //     "user": null,
    //     "good": {
    //         "id": 17,
    //         "category": {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //         },
    //         "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染",
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
    //     "sign_time": "2024-06-19T06:26:17.284Z"
    //     },
    //     {
    //     "id": "w2f82f64-5723-1422-t2cs-2c963f66afa6",
    //     "user": null,
    //     "good": {
    //         "id": 19,
    //         "category": {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //         },
    //         "name": "大猫日记电动旋转猫玩具自动逗猫棒",
    //         "brief_content": "",
    //         "content": "",
    //         "front_image": require('../assets/temp/2.jpg'),
    //         "price": 78.00,
    //         "create_time": "2024-05-23T11:24:17.284Z",
    //         "modify_time": "2024-05-23T11:24:17.284Z",
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
    //     "sign_time": "2024-06-19T06:26:17.284Z"
    //     },
    //     {
    //     "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    //     "user": null,
    //     "good": {
    //         "id": 17,
    //         "category": {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //         },
    //         "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染",
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
    //     "sign_time": "2024-06-19T06:26:17.284Z"
    //     },
    //     {
    //     "id": "w2f82f64-5723-1422-t2cs-2c963f66afa6",
    //     "user": null,
    //     "good": {
    //         "id": 19,
    //         "category": {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //         },
    //         "name": "大猫日记电动旋转猫玩具自动逗猫棒",
    //         "brief_content": "",
    //         "content": "",
    //         "front_image": require('../assets/temp/2.jpg'),
    //         "price": 78.00,
    //         "create_time": "2024-05-23T11:24:17.284Z",
    //         "modify_time": "2024-05-23T11:24:17.284Z",
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
    //     "sign_time": "2024-06-19T06:26:17.284Z"
    //     },
    //     {
    //     "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    //     "user": null,
    //     "good": {
    //         "id": 17,
    //         "category": {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //         },
    //         "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染",
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
    //     "sign_time": "2024-06-19T06:26:17.284Z"
    //     },
    //     {
    //     "id": "w2f82f64-5723-1422-t2cs-2c963f66afa6",
    //     "user": null,
    //     "good": {
    //         "id": 19,
    //         "category": {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //         },
    //         "name": "大猫日记电动旋转猫玩具自动逗猫棒",
    //         "brief_content": "",
    //         "content": "",
    //         "front_image": require('../assets/temp/2.jpg'),
    //         "price": 78.00,
    //         "create_time": "2024-05-23T11:24:17.284Z",
    //         "modify_time": "2024-05-23T11:24:17.284Z",
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
    //     "sign_time": "2024-06-19T06:26:17.284Z"
    //     },
    //     {
    //     "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    //     "user": null,
    //     "good": {
    //         "id": 17,
    //         "category": {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //         },
    //         "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染",
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
    //     "sign_time": "2024-06-19T06:26:17.284Z"
    //     },
    //     {
    //     "id": "w2f82f64-5723-1422-t2cs-2c963f66afa6",
    //     "user": null,
    //     "good": {
    //         "id": 19,
    //         "category": {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //         },
    //         "name": "大猫日记电动旋转猫玩具自动逗猫棒",
    //         "brief_content": "",
    //         "content": "",
    //         "front_image": require('../assets/temp/2.jpg'),
    //         "price": 78.00,
    //         "create_time": "2024-05-23T11:24:17.284Z",
    //         "modify_time": "2024-05-23T11:24:17.284Z",
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
    //     "sign_time": "2024-06-19T06:26:17.284Z"
    //     },
    //     {
    //     "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    //     "user": null,
    //     "good": {
    //         "id": 19,
    //         "category": {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //         },
    //         "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染维酸钾片炎症感染",
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
    //     "address": "新日暮里祥和路1919810号",
    //     "signer_name": "马牛逼",
    //     "signer_mobile": "19975765899",
    //     "create_time": "2024-06-19T06:26:17.284Z",
    //     "sign_time": "2024-06-19T06:26:17.284Z"
    //     },
    //     {
    //     "id": "w2f82f64-5723-1422-t2cs-2c963f66afa6",
    //     "user": null,
    //     "good": {
    //         "id": 19,
    //         "category": {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //         },
    //         "name": "大猫日记电动旋转猫玩具自动逗猫棒",
    //         "brief_content": "",
    //         "content": "",
    //         "front_image": require('../assets/temp/2.jpg'),
    //         "price": 78.00,
    //         "create_time": "2024-05-23T11:24:17.284Z",
    //         "modify_time": "2024-05-23T11:24:17.284Z",
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
    //     "sign_time": "2024-06-19T06:26:17.284Z"
    //     },
    // ]
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

.orders-windows{
  background-image: url("../assets/images/home/eshop/order_list.png");
  width: 958px;
  height: 1390px;
}

.orderitem{ 
  background-color: #fff;
  float: left;
  width: 910px;
  height: 140px;
  background: #fff;
  display: flex;
  flex-direction: row;
  margin-left: -15px;
  border-bottom: 1px solid #eeeeee;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.order_box{
  width: 135px;
  height: 135px;
  margin-top: 5px;
  margin-left: 5px;
}

.order-details{
  display: flex; 
  flex-direction: column; 
  margin-left: 20px;
  width: 400px;
  text-align: left;
}

.order-details h5{
  height: 45px;
  font-size: 15px;
  margin-top: 0px;
  margin-bottom: 0px;
}

.order-details p{
  font-size: 14px;
  margin-top: 0px;
  margin-bottom: 5px;
}


</style>
