<!-- 
社区 /community
-->

<template>
  <div class="communityWindow">
    <div class="titlecontent">
      <div style="margin-top: 15px;">
        <el-input placeholder="搜索你感兴趣的内容" v-model="keyWord" class="input-with-select">
          <el-select v-model="select" slot="prepend" 
          placeholder="请选择" style="width: 90px;">
            <el-option label="主题" value="topic"></el-option>
            <el-option label="作者" value="author"></el-option>
          </el-select>
        </el-input>
      </div>
      <el-button type="primary" @click='searchPost(select,keyWord)' class="shopButton" 
          style="background-color: #e55e5e;
                border-color: #e55e5e;">搜索</el-button>
    </div>

    <div class="show">
      <div class="shop-windows">
        <div class="labelPost">
          <ul class="custom-menu">  
            <li  
              class="custom-menu-item"  
              :class="{ 'is-active': activeLabel === 1 }"  
              @click="activeLabel = 1; plabelChange(activeLabel);"  
            >  
              <a href="#">全&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;部</a>  
            </li>  
            <li  
              class="custom-menu-item"  
              :class="{ 'is-active': activeLabel === 2 }"  
              @click="activeLabel = 2; plabelChange(activeLabel);"  
            >  
              <a href="#">宠物健康</a>  
            </li>  
            <li  
              class="custom-menu-item"  
              :class="{ 'is-active': activeLabel === 3 }"  
              @click="activeLabel = 3; plabelChange(activeLabel);"  
            >  
              <a href="#">萌宠日常</a>  
            </li>
            <li  
              class="custom-menu-item"  
              :class="{ 'is-active': activeLabel === 4 }"  
              @click="activeLabel = 4; plabelChange(activeLabel);"  
            >  
              <a href="#">养宠经验</a>  
            </li>
            <button class="postButton" @click="routeNewpost">
              <i class="el-icon-edit-outline" style="margin-right: 5px;"></i>发帖
            </button>
          </ul>  
        </div>

        <div>
          <ul class="order-menu">  
            <li  
              class="order-menu-item"  
              :class="{ 'is-active': activeOrder === 1 }"  
              @click="activeOrder=1; orderPost(activeOrder);" 
            >  
              <a href="#">时间</a>  
            </li>  
            <li  
              class="order-menu-item"  
              :class="{ 'is-active': activeOrder === 2 }"
              @click="activeOrder=2; orderPost(activeOrder);"    
            >  
              <a href="#">回复</a>  
            </li>  
            <li  
              class="order-menu-item"  
              :class="{ 'is-active': activeOrder === 3 }"  
              @click="activeOrder=3; orderPost(activeOrder);" 
            >  
              <a href="#">查看</a>  
            </li>
            <li  
              class="order-menu-item"  
              :class="{ 'is-active': activeOrder === 4 }"  
              @click="activeOrder=4; orderPost(activeOrder);"  
            >  
              <a href="#">收藏</a>  
            </li>
          </ul>  
          <div class="indexshow">
            <p class="pfirst">作者/创建时间</p>
            <p>回复/查看</p>
          </div>
        </div>

        <div class="post-list" style="height: 925px;">
          <ul v-for="(item,index) in paginatedPosts" :key="index" style="list-style-type: none; margin-left: 0px; margin-bottom: 0px; margin-top: 0px;">
              <li class="post">
                <i v-if="item.tag.id===1" class="el-icon-first-aid-kit" style="margin-left: 10px; margin-right: 15px; margin-top: 22px;"></i>
                <i v-if="item.tag.id===2" class="el-icon-sunny" style="margin-left: 10px; margin-right: 15px; margin-top: 22px;"></i>
                <i v-if="item.tag.id===3" class="el-icon-chat-line-square" style="margin-left: 10px; margin-right: 15px; margin-top: 22px;"></i>
                <p class="tag-name">[{{genTagname(item.tag.id)}}]</p>  
                <h4 class="postTitle" @click="routePost(item.id)">{{item.title.length<=47?item.title:item.title.slice(0,47)+'...'}}</h4>
                <div class="postDetails">
                  <div class="author_time">
                    <p class="p_author">{{item.author.username.length<=8?(item.author.username):(item.author.username.slice(0,8)+'...')}}</p>
                    <p class="p_time">{{item.create_time.slice(0, 10)}}</p>
                  </div>
                  <div class="click_comment">
                    <p class="p_comment">{{item.comment_num}}</p>
                    <p class="p_click">{{item.click_num}}</p>
                  </div>
                </div>
              </li>
          </ul>
        </div>

        <div class="pagination">  
            <el-pagination  
              @size-change="handleSizeChange"  
              @current-change="handleCurrentChange"  
              :current-page="currentPage"  
              :page-sizes="[16]"  
              :page-size="pageSize"  
              layout="total, sizes, prev, pager, next, jumper"  
              :total="totalPosts">  
            </el-pagination>  
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import { getPostsList } from '../api/api';
export default {
  name:'community',
  data() {
    return {
      // 当前激活的标签和排序方式
      activeLabel: 1,
      activeOrder: 1,

      // 搜索字段选择 select=topic/author
      keyWord: '',
      select: 'topic',

      // 当前查询约束
      last_constraint: {
        category: null,    // 1=宠物健康 2=萌宠日常 3=养宠经验
        order: 'create_time,click_num,favor_num,comment_num',
        searchkey: '',
        istopic: true, //是否是对title+briefcontent的搜索,反之为对作者的搜索
        isforward: true,  // 排序正逆序 永远正序
      },

      // 待展示的帖子列表
      postList: [],

      // 当前页面， 每页大小（固定，用于请求时做参数）以及帖子数量
      currentPage: 1, 
      pageSize: 16, 
      totalPosts: 0,       
    };
  },
  computed: {  
    // 计算帖子切片分页，可忽略
    paginatedPosts() {  
      const start = (this.currentPage - 1) * this.pageSize;  
      const end = start + this.pageSize;  
      return this.postList.slice(start, end);  
    },  
  },
  methods: {
    // 跳转到帖子详情，可忽略
    routePost(index){
      this.$router.push({name: 'post', params:{id: index}});
    },
    // 跳转到发帖，可忽略
    routeNewpost(){
      const token = Cookies.get(`token`);
      if(token) {
        this.$router.push('/createpost');
      }
      else {
        this.$message.error('未登录用户不能无法发帖，正在跳转到登录页面！');
        this.$router.push('/login');
      }
      
    },
    // 处理页面大小和页码的函数，可忽略
    handleSizeChange(val) {  
      this.pageSize = val;  
    },  
    handleCurrentChange(val) {  
      this.currentPage = val;  
    },

    // 根据tag id 获取打印信息的函数， 可忽略
    genTagname(tag){
      if(tag === 1)
        return '宠物健康'
      if(tag === 2)
        return '萌宠日常'
      if(tag === 3)
        return '养宠经验'
    },

    // 按last_constraint约束条件进行查询
    executePostsearch(){
      this.currentPage = 1;
      let key_word = null;
      let poster = null;
      if(this,this.last_constraint.istopic) {
        key_word = this.last_constraint.searchkey;
      }
      else {
        poster = this.last_constraint.searchkey;
      }
      let tag = '';
      switch(this.last_constraint.category){
        case(1): tag = '1';break;
        case(2): tag = '2';break;
        case(3): tag = '3';break;
        default: //this.$message(`不以标签为约束条件进行查询`);
      }
      const ordering = this.last_constraint.order;
      getPostsList(key_word, poster, tag, undefined, undefined, ordering, 1, 199).then
      (response =>
        {
          if(response.status === 200) {
            // for debug
            // this.$message.success("按last_constrainr条件集查询成功");
            this.totalPosts = response.data.count;
            this.postList = response.data.results;
          }
        }
      ).catch
      (error => 
        {
          console.error('Enquiry Failed', error);
          this.$message.error('在查询帖子列表时发生网络错误，请检查网络状况！');
        }
      )
    },

    // 按搜索字段index维护last_constraint中的istopic，将key传给searchkey
    searchPost(index, key){
      if(index === 'topic') {
        this.last_constraint.istopic = true;
        this.last_constraint.searchkey = key;
        this.executePostsearch();
        // for debug
        this.$message(`选择字段: 主题, 关键词: ${key}`);
      }
      else if(index === 'author'){
        this.last_constraint.istopic = false;
        this.last_constraint.searchkey = key;
        this.executePostsearch();
        // for debug
        this.$message(`选择字段: 作者, 关键词: ${key}`);
      }
    },

    // 按照index维护last_constraint中的category
    plabelChange(index){
      if(index === 1) {
        this.last_constraint.category = null;
        this.executePostsearch();
        // for debug
        this.$message('标签选择: 全部');
      }  
      else if(index === 2){
        this.last_constraint.category = 1;
        this.executePostsearch();
        // for debug
        this.$message('标签选择: 宠物健康');
      }
      else if(index === 3) {
        this.last_constraint.category = 2;
        this.executePostsearch();
        // for debug
        this.$message('标签选择: 萌宠日常');
      }
      else if(index === 4) {
        this.last_constraint.category = 3;
        this.executePostsearch();
        // for debug
        this.$message('标签选择: 养宠经验');
      }
    },

    // 按照index维护last_constraint中的order
    orderPost(index){
      switch(index) {
        case(1):
          this.last_constraint.order = 'create_time,click_num,favor_num,comment_num';
          this.executePostsearch();
          // for debug
          this.$message('排序选择: 时间');
          break;
        case(2):
          this.last_constraint.order = 'comment_num,favor_num,create_time,click_num';
          this.executePostsearch();
          // for debug
          this.$message('排序选择: 回复');
          break;
        case(3):
          this.last_constraint.order = 'click_num,create_time,favor_num,comment_num';
          this.executePostsearch();
          // for debug
          this.$message('排序选择: 查看');
          break;
        case(4):
          this.last_constraint.order = 'favor_num,comment_num,click_num,create_time';
          this.executePostsearch();
          // for debug
          this.$message('排序选择: 收藏');
          break;
        default:
          this.last_constraint.order = 'create_time,click_num,favor_num,comment_num';
          this.executePostsearch();
          // for debug
          this.$message('默认排序：时间');
      }
    },

  },
  mounted() {

  },
  created() {
    // 初始化
    this.executePostsearch();

    // this.totalPosts = 24
    // this.postList = [
    //   {
    //     "id": "0",
    //     "title": "猫咪掉毛严重怎么办？怎么花更少的钱改善猫咪掉毛问题？怎么花更少的钱改善猫咪掉毛问题？怎么花更少的钱改善猫咪掉毛问题？",
    //     "tag": {"id": 1},
    //     "brief_content": "猫咪掉毛严重怎么办",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠今晚打老鼠今晚打老鼠今晚打老鼠"
    //     },
    //     "click_num": 98,
    //     "comment_num": 16,
    //     "favor_num": 20,
    //     "create_time": "2024-06-23T02:13:18.414Z",
    //     "modify_time": "2024-06-23T02:13:18.414Z"
    //   },
    //   {
    //     "id": "1",
    //     "title": "一文读懂|狗狗子宫炎症，对症下药不再愁",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗子宫炎症",
    //     "author": {
    //       "id": 16,
    //       "username": "清秋自有梧桐在"
    //     },
    //     "click_num": 236,
    //     "comment_num": 32,
    //     "favor_num": 60,
    //     "create_time": "2024-03-21T02:13:18.414Z",
    //     "modify_time": "2024-03-21T02:13:18.414Z"
    //   },
    //   {
    //     "id": "2",
    //     "title": "狗狗身上有跳蚤怎么办？光驱虫是没用的！",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗跳蚤",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "3",
    //     "title": "猫咪掉毛严重怎么办？怎么花更少的钱改善猫咪掉毛问题？",
    //     "tag": {"id": 1},
    //     "brief_content": "猫咪掉毛严重怎么办",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 98,
    //     "comment_num": 16,
    //     "favor_num": 20,
    //     "create_time": "2024-06-23T02:13:18.414Z",
    //     "modify_time": "2024-06-23T02:13:18.414Z"
    //   },
    //   {
    //     "id": "4",
    //     "title": "一文读懂|狗狗子宫炎症，对症下药不再愁",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗子宫炎症",
    //     "author": {
    //       "id": 16,
    //       "username": "清秋自有梧桐在"
    //     },
    //     "click_num": 236,
    //     "comment_num": 32,
    //     "favor_num": 60,
    //     "create_time": "2024-03-21T02:13:18.414Z",
    //     "modify_time": "2024-03-21T02:13:18.414Z"
    //   },
    //   {
    //     "id": "5",
    //     "title": "狗狗身上有跳蚤怎么办？光驱虫是没用的！",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗跳蚤",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "6",
    //     "title": "猫咪掉毛严重怎么办？怎么花更少的钱改善猫咪掉毛问题？",
    //     "tag": {"id": 1},
    //     "brief_content": "猫咪掉毛严重怎么办",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 98,
    //     "comment_num": 16,
    //     "favor_num": 20,
    //     "create_time": "2024-06-23T02:13:18.414Z",
    //     "modify_time": "2024-06-23T02:13:18.414Z"
    //   },
    //   {
    //     "id": "7",
    //     "title": "一文读懂|狗狗子宫炎症，对症下药不再愁对症下药不再愁对症下药不再愁对症下药不再愁对症下药不再愁对症下药不再愁",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗子宫炎症",
    //     "author": {
    //       "id": 16,
    //       "username": "清秋自有梧桐在清秋自有梧桐在清秋自有梧桐在清秋自有梧桐在"
    //     },
    //     "click_num": 236,
    //     "comment_num": 32,
    //     "favor_num": 60,
    //     "create_time": "2024-03-21T02:13:18.414Z",
    //     "modify_time": "2024-03-21T02:13:18.414Z"
    //   },
    //   {
    //     "id": "8",
    //     "title": "狗狗身上有跳蚤怎么办？光驱虫是没用的！",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗跳蚤",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "9",
    //     "title": "猫咪掉毛严重怎么办？怎么花更少的钱改善猫咪掉毛问题？",
    //     "tag": {"id": 1},
    //     "brief_content": "猫咪掉毛严重怎么办",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 98,
    //     "comment_num": 16,
    //     "favor_num": 20,
    //     "create_time": "2024-06-23T02:13:18.414Z",
    //     "modify_time": "2024-06-23T02:13:18.414Z"
    //   },
    //   {
    //     "id": "10",
    //     "title": "一文读懂|狗狗子宫炎症，对症下药不再愁",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗子宫炎症",
    //     "author": {
    //       "id": 16,
    //       "username": "清秋自有梧桐在"
    //     },
    //     "click_num": 236,
    //     "comment_num": 32,
    //     "favor_num": 60,
    //     "create_time": "2024-03-21T02:13:18.414Z",
    //     "modify_time": "2024-03-21T02:13:18.414Z"
    //   },
    //   {
    //     "id": "11",
    //     "title": "狗狗身上有跳蚤怎么办？光驱虫是没用的！",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗跳蚤",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "12",
    //     "title": "猫咪掉毛严重怎么办？怎么花更少的钱改善猫咪掉毛问题？",
    //     "tag": {"id": 1},
    //     "brief_content": "猫咪掉毛严重怎么办",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 98,
    //     "comment_num": 16,
    //     "favor_num": 20,
    //     "create_time": "2024-06-23T02:13:18.414Z",
    //     "modify_time": "2024-06-23T02:13:18.414Z"
    //   },
    //   {
    //     "id": "13",
    //     "title": "一文读懂|狗狗子宫炎症，对症下药不再愁",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗子宫炎症",
    //     "author": {
    //       "id": 16,
    //       "username": "清秋自有梧桐在"
    //     },
    //     "click_num": 236,
    //     "comment_num": 32,
    //     "favor_num": 60,
    //     "create_time": "2024-03-21T02:13:18.414Z",
    //     "modify_time": "2024-03-21T02:13:18.414Z"
    //   },
    //   {
    //     "id": "14",
    //     "title": "狗狗身上有跳蚤怎么办？光驱虫是没用的！",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗跳蚤",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "15",
    //     "title": "狗狗身上有跳蚤怎么办？光驱虫是没用的！",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗跳蚤",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "16",
    //     "title": "狗狗身上有跳蚤怎么办？光驱虫是没用的！",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗跳蚤",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "17",
    //     "title": "狗狗身上有跳蚤怎么办？光驱虫是没用的！",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗跳蚤",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "18",
    //     "title": "狗狗身上有跳蚤怎么办？光驱虫是没用的！",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗跳蚤",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "19",
    //     "title": "好奇心极强的狗狗",
    //     "tag": {"id": 2},
    //     "brief_content": "狗狗",
    //     "author": {
    //       "id": 154,
    //       "username": "拆家小能手"
    //     },
    //     "click_num": 965,
    //     "comment_num": 22,
    //     "favor_num": 45,
    //     "create_time": "2024-01-21T02:13:18.414Z",
    //     "modify_time": "2024-01-21T02:13:18.414Z"
    //   },
    //   {
    //     "id": "20",
    //     "title": "巴哥犬饲养指南：制胜关键巴哥犬饲养指南：制胜关键",
    //     "tag": {"id": 3},
    //     "brief_content": "巴哥犬",
    //     "author": {
    //       "id": 16,
    //       "username": "清秋自有梧桐在"
    //     },
    //     "click_num": 126,
    //     "comment_num": 1,
    //     "favor_num": 56,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "21",
    //     "title": "狗狗身上有跳蚤怎么办？光驱虫是没用的！",
    //     "tag": {"id": 1},
    //     "brief_content": "狗狗跳蚤",
    //     "author": {
    //       "id": 15,
    //       "username": "今晚打老鼠"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-04-24T02:13:18.414Z",
    //     "modify_time": "2024-04-25T02:13:18.414Z"
    //   },
    //   {
    //     "id": "22",
    //     "title": "文静的小猫咪",
    //     "tag": {"id": 2},
    //     "brief_content": "猫咪日常",
    //     "author": {
    //       "id": 17,
    //       "username": "随便啦"
    //     },
    //     "click_num": 76,
    //     "comment_num": 26,
    //     "favor_num": 3,
    //     "create_time": "2024-02-12T02:13:18.414Z",
    //     "modify_time": "2024-02-12T02:13:18.414Z"
    //   },
      
    // ]
  },
}
</script>

<style scoped>
body {  
  background-color: #FFFEF5;
}

.communityWindow{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.shop-windows{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  margin-bottom: 30px;
  padding: 0px;
  height: 1100px;
  min-width: 1230px;
  width: 1230px;
  background-image: url("../assets/images/home/community/community_list.png");
}

.titlecontent{
  display: flex;    
  align-items: center;
  margin-top: 10px;
  margin-bottom: 20px;
}

.el-select .el-input {
  width: 130px;
}

.input-with-select{
  width: 1120px;
}

.shopButton{
  background-color: #e55e5e;
  border-color: #e55e5e;
  margin-top: 15px;
  margin-left: 20px;
}

.show {  
  display: flex;  
  justify-content: space-between;
  align-items: flex-start;
  margin-top: 0px;
}

.custom-menu {  
  display: flex;  
  list-style: none;  
  padding: 0;  
  margin-left: 30px;  
  margin-bottom: 0px;
}  
  
.custom-menu-item {   
  position: relative; 
  margin-right: 30px; 
  margin-top: 6px;
  font-size: 15px;
  flex-shrink: 0; 
  text-decoration: none;
  user-select: none; 
  -moz-user-select: none; 
  -ms-user-select: none;
  -webkit-user-select: none; 
}  
  
.custom-menu-item a {  
  text-decoration: none;  
  color: #7A5151; 
  display: inline-block;
  padding-bottom: 10px;   
  padding-top: 8px;
  padding-left: 10px;
  padding-right: 10px;
  background-color: #FFFEF5;
  border: 1px solid #FFFEF5;  
  border-radius: 6px;
}  

.custom-menu-item.is-active a {  
  color: #ffffff;  
  background-color: #e55e5e; 
  padding-top: 8px;
  padding-left: 10px;
  padding-right: 10px;
}

.custom-menu-item:hover a {  
  color: #ffffff;  
  background-color: #e55e5e; 
  padding-top: 8px;
  padding-left: 10px;
  padding-right: 10px;
}  

.postButton{
  margin-left: 650px;
  margin-top: 5px;
  width: 80px;
  height: 40px;
  background-color: transparent;
  border-color: transparent;
  user-select: none; 
  -moz-user-select: none; 
  -ms-user-select: none;
  -webkit-user-select: none; 
  cursor: pointer;
  font-size: 16px;
  color: #A15151;
}

.postButton:hover{
  background-color: #B4D65F;
  color: #ffffff;
}

.order-menu {  
  /* 自定义菜单样式 */  
  display: flex;  
  list-style: none;  
  padding: 0;  
  margin-left: 40px;  
  margin-top: 20px;
}  
  
.order-menu-item {   
  position: relative; 
  margin-right: 30px; 
  margin-top: 0px;
  font-size: 14px;
  flex-shrink: 0; 
  text-decoration: none;
}  
  
.order-menu-item a {  
  text-decoration: none;  
  color: #ffffff; 
  display: inline-block;
  padding-bottom: 10px;   
}  

.order-menu-item.is-active a {  
  color: #ffffff;   
}

.order-menu-item.is-active::after {  
  content: '';  
  position: absolute;  
  left: 0;  
  bottom: 0;  
  width: 100%;  
  height: 4px; 
  background-color: #ffffff;  
}  
  
.order-menu-item:hover a {  
  color: #ffffff;  
}  
  
.order-menu-item:hover::after {  
  content: '';  
  position: absolute;  
  left: 0;  
  bottom: 0;  
  width: 100%;  
  height: 4px; 
  background-color: #ffffff; 
} 

.indexshow{
  display: flex; 
  flex-direction: row; 
  justify-content: flex-end;
  margin-right: 50px;
  margin-top: -58px;
  user-select: none; 
  -moz-user-select: none; 
  -ms-user-select: none;
  -webkit-user-select: none; 
}

.indexshow p{ 
  color: #e9e9e9;
}

.pfirst{
  margin-right: 55px;
}

.post-list{
  display: flex;
  flex-direction: column;
  margin-left: -30px;
  margin-top: 0px;
}

.post{
  display: flex;
  flex-direction: row;
  border-bottom: 1px solid #cfcfcf;  
  height: 55px;
  margin-left: 0px;
  margin-top: 1px;
  margin-bottom: 0px;
  width: 1209px;
}

.tag-name{
  margin-top: 19px;
  margin-right: 10px;
  font-size: 14px;
  margin-bottom: 0px;
}

.postTitle{
  margin-top: 18px;
  margin-bottom: 0px;
  text-align: left;  
  width: 800px;
}

.postTitle:hover{
  color:#EE6F60
}

.postDetails{
  display: flex;
  flex-direction: row;
}

.author_time{
  width: 160px;
  margin-right: 35px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.p_author{
  margin-top: 0px;
  margin-bottom: 5px;
  font-size: 15px;
}

.p_time{
  margin-top: 0px;
  margin-bottom: 0px;
  font-size: 12px;
  color: #878879;
}

.click_comment{
  width: 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.p_comment{
  margin-top: 0px;
  margin-bottom: 5px;
  font-size: 15px;
  color: #e55e5e;
}

.p_click{
  margin-top: 0px;
  margin-bottom: 0px;
  font-size: 12px;
  color: #878879;
}

</style>
