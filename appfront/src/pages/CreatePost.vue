<!-- 
发帖 /createpost
-->

<template>
    <div class="createPost-Window">
      <div v-if="!isConfirm" class="p-detail-windows">
        <div style="margin-top: 65px;">
          <div class="tips_inputs1">
            <p>标题</p>
            <el-input class="title-input" autosize type="textarea" 
              v-model="post.title" maxlength="20"
              show-word-limit>
            </el-input>
            <el-select v-model="tag" placeholder="选择分区" class="tag">
                <el-option label="宠物健康" value="1"></el-option>
                <el-option label="萌宠日常" value="2"></el-option>
                <el-option label="养宠经验" value="3"></el-option>
            </el-select>
          </div>
          <div class="tips_inputs2">
            <p>简介</p>
            <el-input class="brief-input" autosize type="textarea" 
              v-model="post.brief_content" maxlength="99" show-word-limit
              placeholder="填写简介, 让你的话题更易被看见"></el-input>
          </div>
          <div class="tips_inputs3">
            <p>正文</p>
            <el-input class="text-input" autosize type="textarea" 
              v-model="post.content" maxlength="500" show-word-limit></el-input>
          </div>
          <div class="front_confirm">
            <el-button type="primary" :disabled="!isOK" @click="confirmPost"
            :style="{opacity: !isOK ? 0.5 : 1}"
            style="background-color: #e55e5e; height: 40px; width: 120px; margin-left: 800px;
                  border-color: #e55e5e;">发布
              <i class="el-icon-s-promotion"></i>
            </el-button>
          </div>
        </div>
      </div>

      <div v-if="isConfirm" class="p-confirm-windows-ok">
        <h2>{{"发布成功！将在"+confirm_countdown+"s后返回社区"}}</h2>
      </div>
    </div>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import { createNewPost } from "../api/api";
export default {
  name:'createpost',
  data() {
    return {
      post: {
        title: '',
        brief_content: '',
        content: '',
      },
      tag: '',
      front_form: new FormData(),
      confirm_countdown: 3,

      front_image_file: null,

      // 是否点击确认
      isConfirm: false,
    };
  },
  computed:{
    isOK(){
      if(this.post.title.length <= 0 || 
         this.post.brief_content.length <= 0 ||
         this.post.content.length <= 0 ||
         (this.tag!=='1' && this.tag!=='2' && this.tag!=='3')
        )
        return false
      else
        return true
    }
  },
  methods: {
    uploadImage(event){
      this.front_image_file = event.target.files[0];
    },

    // TODO: 新建帖子发送到后端
    // post.title 标题 post.brief_content 简介 post.content 正文
    // tag 对应帖子信息tag.id(1-3 三个标签)
    // front_form 上传图片的变量
    confirmPost(){
      this.isConfirm = true;
      this.front_form.append('front_image', this.front_image_file);
      createNewPost(this.tag, this.post.title, this.post.brief_content, this.post.content).then
      (response =>
        {
          if(response.status === 201) {
            // for debug
            this.$message('发布成功！');
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
          console.error('Fail to Create New Post.', error);
          this.$message.error('发布帖子时发生网络错误，请检查网络状况！');
        }
      )

      // const token = Cookies.get('token');
      // const config = {  
      //   headers: token ? {  
      //       'Content-Type': 'multipart/form-data',
      //       Authorization: `Bearer ${token}`  
      //   } : {}
      // }

      // axios.post(`http://127.0.0.1:8000/api/forum/posts/create/${this.tag}`, this.front_form, config)
      // .then(respond => {
      //   console.log(respond.data);
      // })
      // .catch(error => {
      //   console.error(error);
      //   this.$message.error(`${error.respond.status}`);
      // })

      // 以下为成功新建后跳转的代码 可以把他放到.then里面 
      // 如果用户填写信息有误就不要执行下列内容
      const intervalId = setInterval(() => {  
        if (this.confirm_countdown > 1) {  
          this.confirm_countdown--;  
        } else {  
          clearInterval(intervalId);   
          this.confirm_countdown = 3;
          this.$router.push({ path: "/community" });
        }  
      }, 1000);

    }
  },
  mounted() {

  },
  created() {

  }
}
</script>

<style scoped>
.createPost-Window{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.p-detail-windows{
  background-image: url("../assets/images/home/community/post_new.png");
  width: 967px;
  height: 549px;
  display: flex;
  flex-direction: column;
}

.p-confirm-windows-ok{
  background-image: url("../assets/images/home/community/post_new.png");
  width: 967px;
  height: 549px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.p-detail-windows>>>.el-textarea__inner {
  border: 0;
  resize: none;
  background-color: transparent;
}

.tips_inputs1{
  display: flex;
  flex-direction: row;
  width: 915px;
  height: 28px;
  margin-left: 20px;
  margin-bottom: 30px;
}

.tips_inputs1 p{
  width: 60px;
  margin-top: 8px;
}

.title-input{
  width: 710px;
  height: 28px;
  border: 1px solid #eeeeee;
  padding-bottom: 10px;
  font-size: 16px;
}

.tips_inputs1>>>.el-textarea__inner {  
  font-weight: bold;  
}

.tag{
  width: 150px;
  height: 24px;
}



.tips_inputs2{
  display: flex;
  flex-direction: row;
  width: 915px;
  height: 48px;
  margin-left: 20px;
  margin-bottom: 30px;
}

.tips_inputs2 p{
  width: 60px;
  margin-top: 8px;
}

.brief-input{
  width: 860px;
  height: 48px;
  border: 1px solid #eeeeee;
  padding-bottom: 10px;
  font-size: 16px;
}

.tips_inputs3{
  display: flex;
  flex-direction: row;
  width: 915px;
  height: 240px;
  margin-left: 20px;
  margin-bottom: 30px;
}

.tips_inputs3 p{
  width: 60px;
  margin-top: 8px;
}

.text-input{
  width: 860px;
  height: 240px;
  border: 1px solid #eeeeee;
  padding-bottom: 10px;
  font-size: 16px;
}

.front_confirm{
  display: flex;
  flex-direction: row;
  width: 915px;
  margin-left: 20px;
  margin-bottom: 30px;
}

.front_confirm p{
  width: 60px;
  margin-top: 8px;
}

</style>
