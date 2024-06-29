<!-- 
我的订单 /myorder
-->

<template>
    <div class="OrderWindow">
        <div class="favor-windows">
            <ul v-for="(item,index) in paginatedOrders" :key="index" style="list-style-type: none; margin-top: 20px;">
              <li class="orderitem">
                  <img v-bind:src="item.good.front_image" class="order_box" alt="">
                  <div class="order-details" @click="routeTwice(item)">
                    <h5 v-html="item.good.name" class="ordername"></h5> 
                    <p> 商品分类: {{ genTag(item.good.category.category_type) }}</p>
                    <p> {{item.good.favor_num}}+人已收藏</p>
                    <p> 收藏时间: {{ item.create_time.slice(0, 10)+ ' '+ item.create_time.slice(11, 19) }}</p>
                    <p> 热销价: &yen;{{ item.good.price }}</p>
                  </div>
                  <div style="display: flex; flex-direction: row; width: 400px; justify-content: end; align-items: flex-end; margin-right: 10px;">
                    <el-badge value="下单立抢现金券">
                    <el-button icon="el-icon-shopping-cart-2" type="primary" @click='routeOrder(item)'
                    style="background-color: #FF7100; color: #ffffff;
                    border-color: #FF7100;
                    width: 120px; height: 40px;">立即购买</el-button>
                    </el-badge>
                  </div>


              </li>
            </ul>
        </div>
        <div style="margin-top: -5px; margin-bottom: 30px;">  
          <el-pagination  
            @size-change="handleSizeChange"  
            @current-change="handleCurrentChange"  
            :current-page="currentPage"  
            :page-sizes="[5]"  
            :page-size="pageSize"  
            layout="total, sizes, prev, pager, next, jumper"  
            :total="totalOrders">  
          </el-pagination>  
          </div>
    </div>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import { getFavorGoodList } from "../api/api";
export default {
  name:'myorder',
  data() {
    return {
      favorList: [],

      // 当前页面， 每页大小（固定，用于请求时做参数）以及订单数量
      currentPage: 1, 
      pageSize: 5, 
      totalOrders: 0, 

    };
  },
  computed: {  
    // 计算订单切片分页，可忽略
    paginatedOrders() {  
      const start = (this.currentPage - 1) * this.pageSize;  
      const end = start + this.pageSize;  
      return this.favorList.slice(start, end);  
    },  
  },
  methods: {
    // 获取用户的商品收藏列表
    obtainFavorGoods() {
      getFavorGoodList(null, null, null, null ,null, 'create_time', 1, 199).then
      (response =>
        {
          if(response.status === 200) {
            this.totalOrders = response.data.count;
            this.favorList = response.data.results;
            // for debug
            console.log(`成功获取到您的商品收藏列表！`);
          }
        }
      ).catch
      (error =>
        {
          if(error.response) {
            if(error.response.status === 401) {
              console.error('Unauthorized.', error);
              // for debug
              this.$message.error('很抱歉，您暂未登录，无法查看自己的商品收藏列表！');
              return;
            }
          }
          console.error('Enquiry Failed.', error);
          this.$message.error('查询收藏商品列表时发生网络错误，请检查网络状况！');
        }
      )
    },

    // 处理页面大小和页码的函数，可忽略
    handleSizeChange(val) {  
      this.pageSize = val;  
    },  
    handleCurrentChange(val) {  
      this.currentPage = val;  
    },
    routeOrder(item){
        this.$router.push({name: 'order', params:{id: item.good.id}});
    },
    routeTwice(item){
        this.$router.push({name: 'item', params:{id: item.good.id}});
    },
    genTag(category){
      switch (category) {
        case 1:
          return '宠物零食'
          break;
        case 2:
          return '宠物玩具'
          break;
        case 3:
          return '宠物药品'
          break;
        default:
          break;
      }
    },
  },
  mounted() {

  },
  created() {
    // 初始化：获取用户的收藏商品
    this.obtainFavorGoods();
    // this.totalOrders = 6;
    // this.favorList = [
    //   {
    //     "good": 
    //     {
    //       "id": "0",
    //       "category": 
    //       {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //       },
    //       "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染",
    //       "content": "",
    //       "front_image": require('../assets/temp/1.jpg'),
    //       "price": 49.99,
    //       "create_time": "2024-06-28T03:57:35.490Z",
    //       "modify_time": "2024-06-28T03:57:35.490Z",
    //       "sold_num": 1798,
    //       "click_num": 45466,
    //       "comment_num": 42,
    //       "favor_num": 1609,
    //       "is_new": false,
    //       "is_hot": false,
    //       "is_ship_free": true
    //     },
    //     "create_time": "2024-06-30T12:57:35.490Z"
    //   },
    //   {
    //     "good": 
    //     {
    //       "id": "1",
    //       "category": 
    //       {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //       },
    //       "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染",
    //       "content": "",
    //       "front_image": require('../assets/temp/1.jpg'),
    //       "price": 49.99,
    //       "create_time": "2024-06-28T03:57:35.490Z",
    //       "modify_time": "2024-06-28T03:57:35.490Z",
    //       "sold_num": 1798,
    //       "click_num": 45466,
    //       "comment_num": 42,
    //       "favor_num": 1609,
    //       "is_new": false,
    //       "is_hot": false,
    //       "is_ship_free": true
    //     },
    //     "create_time": "2024-06-29T12:57:35.490Z"
    //   },
    //   {
    //     "good": 
    //     {
    //       "id": "2",
    //       "category": 
    //       {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //       },
    //       "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染",
    //       "content": "",
    //       "front_image": require('../assets/temp/1.jpg'),
    //       "price": 49.99,
    //       "create_time": "2024-06-28T03:57:35.490Z",
    //       "modify_time": "2024-06-28T03:57:35.490Z",
    //       "sold_num": 1798,
    //       "click_num": 45466,
    //       "comment_num": 42,
    //       "favor_num": 1609,
    //       "is_new": false,
    //       "is_hot": false,
    //       "is_ship_free": true
    //     },
    //     "create_time": "2024-06-29T12:57:35.490Z"
    //   },
    //   {
    //     "good": 
    //     {
    //       "id": "3",
    //       "category": 
    //       {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //       },
    //       "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染",
    //       "content": "",
    //       "front_image": require('../assets/temp/1.jpg'),
    //       "price": 49.99,
    //       "create_time": "2024-06-28T03:57:35.490Z",
    //       "modify_time": "2024-06-28T03:57:35.490Z",
    //       "sold_num": 1798,
    //       "click_num": 45466,
    //       "comment_num": 42,
    //       "favor_num": 1609,
    //       "is_new": false,
    //       "is_hot": false,
    //       "is_ship_free": true
    //     },
    //     "create_time": "2024-06-29T12:57:35.490Z"
    //   },
    //   {
    //     "good": 
    //     {
    //       "id": "4",
    //       "category": 
    //       {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //       },
    //       "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染",
    //       "content": "",
    //       "front_image": require('../assets/temp/1.jpg'),
    //       "price": 49.99,
    //       "create_time": "2024-06-28T03:57:35.490Z",
    //       "modify_time": "2024-06-28T03:57:35.490Z",
    //       "sold_num": 1798,
    //       "click_num": 45466,
    //       "comment_num": 42,
    //       "favor_num": 1609,
    //       "is_new": false,
    //       "is_hot": false,
    //       "is_ship_free": true
    //     },
    //     "create_time": "2024-06-29T12:57:35.490Z"
    //   },
    //   {
    //     "good": 
    //     {
    //       "id": "5",
    //       "category": 
    //       {
    //         "name": "",
    //         "description": "",
    //         "category_type": 1
    //       },
    //       "name": "辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染",
    //       "content": "",
    //       "front_image": require('../assets/temp/1.jpg'),
    //       "price": 49.99,
    //       "create_time": "2024-06-28T03:57:35.490Z",
    //       "modify_time": "2024-06-28T03:57:35.490Z",
    //       "sold_num": 1798,
    //       "click_num": 45466,
    //       "comment_num": 42,
    //       "favor_num": 1609,
    //       "is_new": false,
    //       "is_hot": false,
    //       "is_ship_free": true
    //     },
    //     "create_time": "2024-06-29T12:57:35.490Z"
    //   },
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

.favor-windows{
  background-image: url("../assets/images/home/eshop/myfavor_list.png");
  width: 958px;
  height: 864px;
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

.order-details:hover p{
  color: #ee6f60;
}


</style>
