<!-- 
商品详情 /item/:id
-->

<template>
    <div class="ItemWindow">
      <div class="detail-windows">
        <img v-bind:src="item.image_url" class="item_img" alt="">
        <div class="item_details">
          <h3>{{item.title}}</h3>
          <p>已卖出{{ item.sold_num }}+份</p>
          <div class="item_price">
            <p>&yen;{{item.price}}</p>
          </div>
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
          <div class="item_list">
            <p style="color: #7a7a7a; margin-right: 10px;">点击量: </p>
            <p style="margin-right: 50px; margin-top: 7px;">{{item.click_num}}</p>
          </div>
          <div class="item_list">
            <p style="color: #7a7a7a; margin-right: 10px;">收藏数: </p>
            <p style="margin-right: 50px; margin-top: 7px;">{{item.favor_num}}</p>
          </div>
          <div>
            <el-button icon="el-icon-shopping-cart-1" type="primary" @click='buyItem' class="buyButton"
              style="background-color: #FF7100;
              border-color: #e55e5e;">
              立即购买</el-button>
            <el-button v-if="!isFavor" icon="el-icon-star-off" type="primary" @click='favorItem' class="buyButton"
              style="background-color: #ffffff; color: #000000;
              border-color: #000000;">收藏商品</el-button>
            <el-button v-else icon="el-icon-star-on" type="primary" @click='favorItem' class="buyButton"
              style="background-color: #e55e5e; color: #ffffff
              border-color: #e55e5e;">取消收藏</el-button>
          </div>
        </div>
      </div>

      <div v-if="haveComment" class="comment-windows">
        <div class="allComments" style="margin-top: 80px; height: 410px; margin-bottom: 60px;">
          <ul v-for="(comment,index) in paginatedComments" :key="index" style="list-style-type: none; margin-left: 0px; margin-top: 0px;">
              <li class="comment">
                  <div class="user_info">
                    <div class="avatar_box"><img v-bind:src=avatar_default alt=""></div>
                    <div class="username_time">
                      <h5 v-html="comment.user.username" class="title"></h5> 
                      <h5 v-html="comment.create_time.slice(0,10)+' '+comment.create_time.slice(11,16)" class="create_time"></h5> 
                    </div>
                  </div>
                  <el-rate
                    v-model="comment.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}"
                    style="text-align: left;">
                  </el-rate>
                  <p v-html="comment.content" style="text-align: left; margin-top: 5px;"></p>
              </li>
          </ul>
        </div>
        <div class="pagination">  
          <el-pagination  
            @size-change="handleSizeChange"  
            @current-change="handleCurrentChange"  
            :current-page="currentPage"  
            :page-sizes="[3]"  
            :page-size="pageSize"  
            layout="total, sizes, prev, pager, next, jumper"  
            :total="totalComments">  
          </el-pagination>  
        </div>
      </div>

      <div v-if="!haveComment" class="no-comment-windows"></div>

    </div>
</template>

<script>
import axios from "axios";
import { getSingleGood, favorGood, getFavorGoodList, getGoodCommentList } from "../api/api";
import Cookies from 'js-cookie';
export default {
  name:'item',
  data() {
    return {
      // 显示当前商品是否收藏过，不影响api调用
      isFavor: false,

      // 当前商品是否有评论，如果没有则直接显示暂无评论，节省空间
      totalComments: 0, 
      
      // 商品详细信息
      item: 
      {
        'id': null,
        'title': '',
        'sold_num': 0,
        'price': 0, 
        'image_url': null,
        'is_ship_free': false,
        'is_new': false,
        'is_hot': false,
        'favor_num': 0,
        'click_num': 0,
        'brief_content': null,
        'content': null,
      },

      // 评论信息列表
      respond_comment: [],

      // 登录标志，用于后端交互
      login_flag: false,

      // 默认头像
      avatar_default: require('../assets/images/logo.png'),

      // 评论分页相关
      currentPage: 1, 
      pageSize: 3, 
      haveComment: false,
    };
  },
  computed: {  
    // 计算切片分页，可忽略
    paginatedComments() {  
      const start = (this.currentPage - 1) * this.pageSize;  
      const end = start + this.pageSize;  
      return this.respond_comment.slice(start, end);  
    },  
  },
  methods: {
    // 跳转到购买页面
    buyItem()
    {
      if(this.login_flag)
        this.$router.push({name: 'order', params:{id: this.item.id}});
      else{
        this.$message('未登录用户无法购买商品，正在跳转到登录界面~');
        this.$router.push('/login');
      }
    },

    // 处理页面大小和页码的函数，可忽略
    handleSizeChange(val) 
    {  
      this.pageSize = val;  
    },  
    handleCurrentChange(val) 
    {  
      this.currentPage = val;  
    },

    // 获取商品详细信息
    obtainGoodDetails()
    {
      const good_id = this.item.id;
      getSingleGood(good_id).then
      (response => 
        {
          if(response.status === 200) {
            // for debug
            // this.$message('获取商品详情成功！');
            this.item.title = response.data.name;
            this.item.sold_num =  response.data.sold_num;
            this.item.price = response.data.price;
            this.item.image_url = response.data.front_image;
            this.item.is_ship_free = response.data.is_ship_free;
            this.item.is_hot = response.data.is_hot;
            this.item.is_new = response.data.is_new;
            this.item.click_num = response.data.click_num;
            this.item.favor_num = response.data.favor_num;
          }
        }
      ).catch
      (error =>
        {
          console.error('Enquiry Failed.', error);
          this.$message.error('查询失败，请检查网络状况！');
        }
      )
    },

    favorItem()
    {
      var favored_goods_id = [];
      let favor_flag = false;
      getFavorGoodList('', '', '', undefined, undefined, 'create_time', 1, 199).then
      (response =>
        {
          if(response.status === 200) {
            // for debug
            // this.$message('您已登录');
            this.login_flag = true;
            // 提取该用户点赞过的商品id列表
            if(response.data.count !== 0){
              for(var i = 0; i < response.data.count; i++){
                favored_goods_id.push(response.data.results[i].good.id);  
              }
            }
          }
        }
      ).catch
      (error =>
        {
          if(error.response) {
            if(error.response.status === 401) {
              console.error('Unauthorized.', error);
              // for debug
              // this.$message.error('很抱歉，您暂未登录，无法查看自己的收藏列表！');
              return;
            }
          }
          console.error('Enquiry Failed.', error);
          this.$message.error('查询您的收藏列表时发生网络错误，请检查网络状况！');
        }
      )
      
      // 遍历用户点赞过的商品id列表，设置this.isFavor
      for(var j = 0; j < favored_goods_id.length; j++) {
        if(this.item.id === favored_goods_id[j]) {
          favor_flag = true;
          break;
        }
      }
      if(favor_flag) {
        this.isFavor = true;
      }

      if(this.login_flag) {
        this.isFavor = !this.isFavor;
        if(this.isFavor)
        {
          favorGood(this.item.id);
          // for debug
          // this.$message("favor当前商品");
        }
        else
        {
          favorGood(this.item.id);
          // for debug
          // this.$message("取消favor当前商品")
        }
      }
      else {
        this.$message('未登录用户无法收藏商品，正在跳转到登录界面~');
        this.$router.push('/login');
      }
    },

    favorInit(is_login)
    {
      if(is_login) {
        getFavorGoodList('', '', '', undefined, undefined, 'create_time', 1, 199).then
        (response =>
          {
            let favored_goods = [];
            let favor_flag = false;
            if(response.status === 200) {
              // 提取该用户点赞过的商品id列表
              if(response.data.count !== 0){
                for(var i = 0; i < response.data.count; i++){
                  favored_goods.push(response.data.results[i].good.id);  
                }
                // 遍历用户点赞过的商品id列表，设置this.isFavor
                for(var j = 0; j < favored_goods.length; j++) {
                  if(this.item.id === favored_goods[j]) {
                    favor_flag = true;
                    break;
                  }
                }
              }
            }
            if(favor_flag) {
                this.isFavor = true;
            }
          }
        )
      }
    },

    obtainCommentDetails()
    {
      getGoodCommentList(this.item.id, '', '', undefined, '', '', 'create_time,modify_time,rating', 1, 199).then
      (response =>
        {
          if(response.status === 200) {
            this.totalComments = response.data.count;
            this.respond_comment = response.data.results;
            for(var i = 0; i < this.respond_comment.length; i++){
              switch(response.data.results[0].rating) {
                case('RatingEnum.五星') : this.respond_comment[0].rating = 5;break;
                case('RatingEnum.四星') : this.respond_comment[0].rating = 4;break;
                case('RatingEnum.三星') : this.respond_comment[0].rating = 3;break;
                case('RatingEnum.二星') : this.respond_comment[0].rating = 2;break;
                case('RatingEnum.一星') : this.respond_comment[0].rating = 1;break;
                default:this.respond_comment[0].rating = 0;
              }
            }
            if(response.data.count !== 0) {
              this.haveComment = true;
            }
            // for debug
            // this.$message.success(`成功获取到评论列表！`);
          }
        }
      ).catch
      (error => 
        {
          console.error('Enquiry Failed.', error);
          this.$message.error('查询该商品的评论列表时发生网络错误，请检查网络状况！');
        }
      )
    },

  },
  mounted() {

  },
  created() {
    // 获取当前商品的id(已完成)
    const {id} = this.$route.params
    this.item.id = id

    // 获取用户登录信息
    const token = Cookies.get('token');
    if(token) {
      this.login_flag = true;
    }

    // 获取当前商品的详细信息
    this.obtainGoodDetails(id);

    // 为展示用，以下数据被写死
    // this.item.title = '辉瑞速诺阿莫西林克拉维酸钾片炎症感染辉瑞速诺阿莫西林克拉维酸钾片炎症感染';
    // this.item.sold_num =  1798;
    // this.item.price = 49.99;
    // this.item.image_url = require('../assets/temp/1.jpg');
    // this.item.is_ship_free = true;
    // this.item.is_hot = true;
    // this.item.is_new = true;
    // this.item.click_num = 45466;
    // this.item.favor_num = 1609;

    // 获取当前商品的点赞信息
    this.favorInit(this.login_flag);

    // 获取评论总个数 以及评论的列表

    this.obtainCommentDetails();
    // 测试数据
    // this.totalComments = 7;
    // this.respond_comment = 
    //   [
    //     {
    //       'id': 1,
    //       'user':
    //         {
    //           'username': '两年前被西方社区糕手称为怪物的一名国人玩家'
    //         },
    //       'good': null,
    //       'rating': 4,
    //       'content': '我不愿游戏贴吧整这种烂事, 我的个人频道则无所谓, 此评论与商品并非有关。',
    //       'create_time': "2024-06-16T03:19:27.852Z",
    //       "modify_time": "2024-06-16T03:19:27.852Z"
    //     },
    //     {
    //       'id': 2,
    //       'user':
    //         {
    //           'username': '下头太刀'
    //         }, 
    //       'good': null,
    //       'rating': 2,
    //       'content': '受不了了, 我直接把罗利內酷套我头上，此评论与商品无关。',
    //       'create_time': "2024-06-14T03:19:27.852Z",
    //       "modify_time": "2024-06-15T03:19:27.852Z"
    //     },
    //     {
    //       'id': 3,
    //       'user':
    //         {
    //           'username': '神也会流血吗'
    //         },
    //       'good': null,
    //       'rating': 5,
    //       'content': '好吃. 美味！',
    //       'create_time': "2024-05-03T03:19:27.852Z",
    //       "modify_time": "2024-05-23T03:19:27.852Z"
    //     },
    //     {
    //       'id': 4,
    //       'user':
    //         {
    //           'username': '并非nep'
    //         },
    //       'good': null,
    //       'rating': 1,
    //       'content': 'Hello, everybody. I am speaking English now.',
    //       'create_time': "2024-05-03T03:19:27.852Z",
    //       "modify_time": "2024-05-23T03:19:27.852Z"
    //     },
    //     {
    //       'id': 5,
    //       'user':
    //         {
    //           'username': '并非nep'
    //         },
    //       'good': null,
    //       'rating': 1,
    //       'content': 'Hello, everybody. I am speaking English now.',
    //       'create_time': "2024-05-03T03:19:27.852Z",
    //       "modify_time": "2024-05-23T03:19:27.852Z"
    //     },
    //     {
    //       'id': 6,
    //       'user':
    //         {
    //           'username': '并非有辛并'
    //         },
    //       'good': null,
    //       'rating': 4,
    //       'content': '并, 并非！并, 并非！并, 并非！并, 并非！并, 并非！并, 并非！并, 并非！并, 并非！并, 并非！并, 并非！并, 并非！并, 并非！并, 并非！',
    //       'create_time': "2024-05-03T03:19:27.852Z",
    //       "modify_time": "2024-05-23T03:19:27.852Z"
    //     },
    //     {
    //       'id': 7,
    //       'user':
    //         {
    //           'username': '林晓泽'
    //         },
    //       'good': null,
    //       'rating': 5,
    //       'content': '轮到我来驾驶E萌宠了吗？',
    //       'create_time': "2024-02-13T03:19:27.852Z",
    //       "modify_time": "2024-04-23T03:19:27.852Z"
    //     },
    //   ]
  }
}
</script>

<style scoped>
body {  
  background-color: #FFFEF5; /* 你想要的颜色 */  
}

.ItemWindow{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.detail-windows{
  display: flex;
  flex-direction: row;
  background-image: url("../assets/images/home/eshop/item_list.png");
  width: 950px;
  height: 530px;
}

.comment-windows{
  display: flex;
  flex-direction: column;
  background-image: url("../assets/images/home/eshop/item_comment.png");
  width: 990px;
  height: 600px;
}

.no-comment-windows{
  display: flex;
  flex-direction: column;
  background-image: url("../assets/images/home/eshop/item_no_comment.png");
  width: 990px;
  height: 140px;
}


.item_img{
  width: 460px;
  height: 460px;
  margin-top: 40px;
  margin-left: 40px;
}

.item_details{
  display: flex;
  margin-top: 20px;
  flex-direction: column;
  width: 400px;
  margin-left: 30px;
}

.item_details h3{
  text-align: left;
  margin-bottom: 0px
}
.item_details p{
  margin-top: 8px;
  text-align: left;
  font-size: 14px;
  color: #7a7a7a;
}

.item_price{
  background-image: url("../assets/images/home/eshop/price_bg.png");
  background-size: cover;
  width: 400px;
  height: 100px;
  margin-left: -5px;
  margin-top: -5px;
  margin-bottom: 10px;
}

.item_price p{
  margin-left: 25px;
  margin-top: 55px;
  font-size: 25px;
  color: rgb(253, 59, 59);
}

.item_list{
  display: flex;
  flex-direction: row;
  margin-top: 0px;
}

.item_list p{
  font-size: 15px;
  color: black;
  margin-top: 5px;
}

.buyButton{
  background-color: #e55e5e;
  border-color: #e55e5e;
  width: 195px;
  margin-left: 0px;
}

.comment{
  width: 900px;
  height: auto;
  margin-top: 0px;
  margin-left: 15px;
  margin-bottom: 25px;
  border-bottom: 1px solid #eeeeee;
  padding-bottom: 10px;
}

.user_info{
  display: flex;
  flex-direction: row;
}

.avatar_box{
  width: 60px;
  height: 60px;
  margin-right: 10px;
}

.avatar_box img{
  width: 50px;
  height: 50px;
}

.username_time{
  display: flex;
  flex-direction: column;
  margin-top: 6px;
}

.title{
  font-size: 15px;
  margin-top: 0px;
  margin-bottom: 0px;
  text-align: left;
  height: 20px;
}

.create_time{
  font-size: 13px;
  text-align: left;
  color: #7a7a7a;
  margin-top: 10px;
  margin-bottom: 0px;
  
}


</style>
