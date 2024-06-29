<!-- 
个人中心 /myinfo
待完善功能：
    1. script里的计算属性isDoctor 判断用户是否是医生 如果是返回true 否则返回false 
       如果后面需要用这个变量 可将其赋值给一个this变量再使用
    2. create() 获取用户信息 (医生的接诊信息)
    3. uploadImage() confirmImg() 上传头像
    4. confirmInfo() 提交患者实名信息
    5. confirmAppoint() 提交医生接诊时间
    6. switchStatus() 处于接诊状态的医生关闭接诊
-->

<template>
    <div class="infoWindow">
        <div v-if="!isDoctor" class="info_bg">
            <div class="info_details">
                <p class="tip_info">平台承诺绝不会以任何形式向第三方透漏你的身份信息</p>
                <div class="img_info">
                    <p>头像</p>
                    <img v-bind:src=avatar alt="">
                </div>
                <div class="username_info">
                    <p>用户名</p>
                    <el-input class="username_input" autosize type="textarea" 
                        v-model="username" disabled></el-input>
                </div>
                <div class="email_info" 
                    style="border-bottom: 1px solid #ececec; padding-bottom: 30px;">
                    <p>邮箱</p>
                    <el-input class="email_input" autosize type="textarea" 
                        v-model="email" disabled></el-input>
                </div>
                <div class="email_info">
                    <p>姓名</p>
                    <el-input class="email_input" autosize maxlength="10" type="textarea" 
                        v-model="name"></el-input>
                </div>
                <div class="email_info">
                    <p style="width: 70px; margin-left: 8px">身份证号</p>
                    <el-input style="margin-left: 25px;" class="email_input" autosize type="textarea" 
                        v-model="idno" maxlength="18"></el-input>
                </div>
                <div class="username_info">
                    <p>手机号</p>
                    <el-input class="username_input" autosize type="textarea" 
                        v-model="tel" maxlength="11"></el-input>
                </div> 
                <el-button type="primary" @click="confirmInfo(name, idno, tel)"
                :style="{opacity: !isOK?0.5:1}" :disabled="!isOK"
                style="background-color: #e55e5e; height: 40px; 
                    width: 120px; margin-left: 30px; margin-top: 30px;
                    border-color: #e55e5e;">保存
                <i class="el-icon-check"></i>
                </el-button>
            </div>
        </div>

        <div v-if="isDoctor" class="info_bg2">
            <div class="info_details2">
                <p class="tip_info">平台承诺绝不会以任何形式向第三方透漏你的身份信息</p>
                <div class="img_info">
                    <p>头像</p>
                    <img v-bind:src=avatar alt="">
                </div>
                <div class="username_info">
                    <p>用户名</p>
                    <el-input class="username_input" autosize type="textarea" 
                        v-model="username" disabled></el-input>
                </div>
                <div class="email_info">
                    <p>邮箱</p>
                    <el-input class="email_input" autosize type="textarea" 
                        v-model="email" disabled></el-input>
                </div>
                <div class="email_info">
                    <p>姓名</p>
                    <el-input class="email_input" autosize maxlength="10" type="textarea" 
                        v-model="name" disabled></el-input>
                </div>
                <div class="email_info">
                    <p style="width: 70px; margin-left: 8px">身份证号</p>
                    <el-input style="margin-left: 25px;" class="email_input" autosize type="textarea" 
                        v-model="idno" maxlength="18" disabled></el-input>
                </div>
                <div class="username_info" style="border-bottom: 1px solid #ececec; padding-bottom: 30px;">
                    <p>手机号</p>
                    <el-input class="username_input" autosize type="textarea" 
                        v-model="tel" maxlength="11" disabled>
                    </el-input>
                </div> 
                <div class="username_info">
                    <p style="width: 100px;">是否开启接诊</p>
                    <el-switch v-model="appoiOpen" active-color="#e55e5e"
                    inactive-color="#bebebe" style="margin-left: 10px; margin-top: 12px;"
                    @change="switchStatus"></el-switch>
                </div> 
                <el-table :data="tableData" border class="tableContainer" 
                :row-style="{height: '350px'}"
                :cell-style="{'text-align':'center'}"
                style="width: 841px; margin-left: 25px; max-height: 400px;
                user-select: none; -moz-user-select: none; -ms-user-select: none;
                -webkit-user-select: none; ">
                <el-table-column  prop="day1" label="星期一" width="120">
                    <template slot-scope="scope">
                        <p class="wrap-text">{{ scope.row.day1 }}</p>
                    </template>
                </el-table-column>
                <el-table-column  prop="day2" label="星期二" width="120">
                    <template slot-scope="scope">
                        <p class="wrap-text">{{ scope.row.day2 }}</p>
                    </template>
                </el-table-column>
                <el-table-column  prop="day3" label="星期三" width="120">
                    <template slot-scope="scope">
                        <p class="wrap-text">{{ scope.row.day3 }}</p>
                    </template>
                </el-table-column>
                <el-table-column  prop="day4" label="星期四" width="120">
                    <template slot-scope="scope">
                        <p class="wrap-text">{{ scope.row.day4 }}</p>
                    </template>
                </el-table-column>
                <el-table-column  prop="day5" label="星期五" width="120">
                    <template slot-scope="scope">
                        <p class="wrap-text">{{ scope.row.day5 }}</p>
                    </template>
                </el-table-column>
                <el-table-column  prop="day6" label="星期六" width="120">
                    <template slot-scope="scope">
                        <p class="wrap-text">{{ scope.row.day6 }}</p>
                    </template>
                </el-table-column>
                <el-table-column  prop="day7" label="星期日" width="120">
                    <template slot-scope="scope">
                        <p class="wrap-text">{{ scope.row.day7 }}</p>
                    </template>
                </el-table-column>
                </el-table>
                <div class="addOpenButtons">
                    <el-button icon="el-icon-plus" type="primary" :style="{opacity: !appoiOpen||init?0.5:1}" :disabled="!appoiOpen||init"
                        @click="weekday='day1';dialogFormVisible=true">接诊时间记录
                    </el-button>
                    <el-button icon="el-icon-plus" type="primary" :style="{opacity: !appoiOpen||init?0.5:1}" :disabled="!appoiOpen||init"
                        @click="weekday='day2';dialogFormVisible=true">接诊时间记录
                    </el-button>
                    <el-button icon="el-icon-plus" type="primary" :style="{opacity: !appoiOpen||init?0.5:1}" :disabled="!appoiOpen||init"
                        @click="weekday='day3';dialogFormVisible=true">接诊时间记录
                    </el-button>
                    <el-button icon="el-icon-plus" type="primary" :style="{opacity: !appoiOpen||init?0.5:1}" :disabled="!appoiOpen||init"
                        @click="weekday='day4';dialogFormVisible=true">接诊时间记录
                    </el-button>
                    <el-button icon="el-icon-plus" type="primary" :style="{opacity: !appoiOpen||init?0.5:1}" :disabled="!appoiOpen||init"
                        @click="weekday='day5';dialogFormVisible=true">接诊时间记录
                    </el-button>
                    <el-button icon="el-icon-plus" type="primary" :style="{opacity: !appoiOpen||init?0.5:1}" :disabled="!appoiOpen||init"
                        @click="weekday='day6';dialogFormVisible=true">接诊时间记录
                    </el-button>
                    <el-button icon="el-icon-plus" type="primary" :style="{opacity: !appoiOpen||init?0.5:1}" :disabled="!appoiOpen||init"
                        @click="weekday='day7';dialogFormVisible=true">接诊时间记录
                    </el-button>
                </div>
                <el-dialog class="timeDialog" title="选择当天接诊时段" :visible.sync="dialogFormVisible">
                    <el-transfer v-model="tvalue" :data="tdata" class="timeTransfer"
                    :titles="['备选时间段', '已选时间段']">
                        <el-button class="timeConfirm" 
                            style="border: transparent; background-color: transparent; cursor: default;" 
                            slot="left-footer" size="small"></el-button>
                        <el-button class="timeConfirm" slot="right-footer" @click="submitSelect(tvalue)">确认</el-button>
                    </el-transfer>
                </el-dialog>
                <div class="controlOpenButtons">
                    <el-button icon="el-icon-upload2" type="primary" :style="{opacity: !appoiOpen||init?0.5:1}" :disabled="!appoiOpen||init"
                        @click="confirmAppoint">提交接诊时间
                    </el-button>
                    <el-button icon="el-icon-delete" type="primary" :style="{opacity: !appoiOpen||init?0.5:1}" :disabled="!appoiOpen||init"
                        @click="tvalue=[];clearShow();">清空接诊时间
                    </el-button>
                    <div class="doctorTip">
                      <h3>提示: </h3>
                      <p>1.处于未接诊状态时, 打开“是否接诊”并提交接诊时间, 您的信息即可被患者访问。提交后将无法修改接诊时间。</p>
                      <p>2.将“开启接诊”关闭后方可重新编辑，编辑结果将在本周的下下周生效。修改接诊时间不影响已生效的患者预约。</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
  import axios from "axios";
  import Cookies from "js-cookie";
  import { createNewPatient, getSingleDoctor, updateDoctor, createNewTimetable_doctor, getSingleUser, getDoctorTimetable } from "../api/api";
  import { abortDoctorTimetable } from "../api/api";
  export default {
  name:'myinfo',
  data() {
    const generateData = _ => {
        const data = [];
        for (let i = 0; i < 9; i++) {
          data.push({
            key: i,
            label: `0${i}:00-0${i+1}:00`,
            disabled: false
          });
        }
        data.push({
            key: 9,
            label: `09:00-10:00`,
            disabled: false
          });
        for (let i = 10; i < 23; i++) {
          data.push({
            key: i,
            label: `${i}:00-${i+1}:00`,
            disabled: false
          });
        }
        data.push({
            key: 23,
            label: `23:00-24:00`,
            disabled: false
          });
        return data;
    };
    return {
        avatar_default: require('../assets/images/logo.png'),

        userid: null,
        username: '',
        avatar: '',
        email: '',
        name: '',
        idno: '',
        tel: '',
        openTime: [],

        // 医生信息
        doctor_id: null,
        doctor_origin: null,

        // 是否开启了接诊(接诊==提交了接诊时间，不存在接诊但未提交时间的情况)
        appoiOpen: false,
        init: false,

        dialogFormVisible: false,
        tdata: generateData(),
        tvalue: [],
        weekday: 0,
        avatar_new: new FormData(),
        
        tableData: [{
          day1: this.genOpenTime(''),
          day2: this.genOpenTime(''),
          day3: this.genOpenTime(''),
          day4: this.genOpenTime(''),
          day5: this.genOpenTime(''),
          day6: this.genOpenTime(''),
          day7: this.genOpenTime(''),
        }],
        preData: {
            day1: [],
            day2: [],
            day3: [],
            day4: [],
            day5: [],
            day6: [],
            day7: [],
        }

    };
  },
  methods: {
    // 显示接诊时间文字，忽略
    genOpenTime(str){
      if(str === '')
        return '暂无接诊时间'
      else
        return str
    },

    // 计算接诊时间，忽略
    submitSelect(value){
        value.sort((a, b) => a - b);
        let mergedRanges = []; 
        let currentRangeStart = null; 
        let lastRangeStart = null;
        for (let i = 0; i < value.length; i++) {  
        const currentTime = value[i];   
        if (currentRangeStart === null || currentTime !== (lastRangeStart + 1)) 
        {  
            currentRangeStart = currentTime;  
            lastRangeStart = currentTime;
            mergedRanges.push(this.formatTimeRange(currentRangeStart, currentTime+1));  
        }  
        
        else
        {
            lastRangeStart = currentTime;
            mergedRanges[mergedRanges.length - 1] = this.formatTimeRange(currentRangeStart, currentTime + 1);   
        }  
        }
        this.createShow(mergedRanges);
        this.dialogFormVisible = false;
    },
    formatTimeRange(start, end) {  
        const startHour = this.padZero(start);  
        const endHour = this.padZero(end);
        return `${startHour}:00-${endHour}:00`;  
    },  
    padZero(num) {  
        return num.toString().padStart(2, '0');  
    },
    createShow(pre_str){
      const date = this.weekday;
      this.preData[date] = pre_str
      let ap_str = '';
      for (let i = 0; i < pre_str.length; i++) 
      {
        ap_str = ap_str+pre_str[i]+'\n'
      }
      this.tableData[0][date] = this.genOpenTime(ap_str)
    },
    clearShow(){
      const keys = ['day1','day2','day3','day4','day5','day6','day7']
      this.tvalue = []
      for (let i = 0; i < keys.length; i++) 
      {
          this.tableData[0][keys[i]] = this.genOpenTime('');
          this.preData[keys[i]] = [];
      }


    },
    front2back(frontData){
      let results = []
      const keys = ['day1','day2','day3','day4','day5','day6','day7']
      for(let i = 0; i < keys.length; i++)
      {
        let weekday = i+1;
        for(let j = 0; j < frontData[keys[i]].length; j++)
        {
            let raw = frontData[keys[i]][j];
            let start_time = raw.slice(0,5)+":00"
            let end_time = raw.slice(6,11)+":00"
            if(end_time === '24:00:00')
                end_time = '23:59:59'
            let result = {
                "day_of_week": weekday,
                "start_time": start_time,
                "end_time": end_time
            }
            results.push(result)
        } 
      }
      return results
    },
    hanzi2keys(ph)
    {
        switch (ph) {
            case 'DayOfWeekEnum.星期一':
                return 'day1'
                break;
            case 'DayOfWeekEnum.星期二':
                return 'day2'
                break;
            case 'DayOfWeekEnum.星期三':
                return 'day3'
                break;
            case 'DayOfWeekEnum.星期四':
                return 'day4'
                break;
            case 'DayOfWeekEnum.星期五':
                return 'day5'
                break;
            case 'DayOfWeekEnum.星期六':
                return 'day6'
                break;
            default:
                return 'day7'
                break;
        }
    },
    back2front(backData){
      let lastWeekday = 'day0';
      let templist = [];
      for(let i = 0; i < backData.length; i++)
      {
        let pre_str = backData[i];
        this.weekday = this.hanzi2keys(pre_str.day_of_week)
        console.log(`${this.weekday}`)
        if(lastWeekday === this.weekday)
        {
            if(pre_str.end_time === '23:59:59')
                pre_str.end_time = '24:00:00';
            templist.push(pre_str.start_time.slice(0,5)+'-'+pre_str.end_time.slice(0,5));
            if(i === backData.length-1)
                this.createShow(templist)
        }
        else
        {

            if(lastWeekday !== 'day0')
            {
                this.weekday = lastWeekday;
                this.createShow(templist);
                this.weekday = this.hanzi2keys(pre_str.day_of_week)
                templist = []
                if(pre_str.end_time === '23:59:59')
                    pre_str.end_time = '24:00:00';
                templist.push(pre_str.start_time.slice(0,5)+'-'+pre_str.end_time.slice(0,5));
                if(i === backData.length-1)
                    this.createShow(templist)
                
            }
            else
            {
                if(pre_str.end_time === '23:59:59')
                    pre_str.end_time = '24:00:00';
                templist.push(pre_str.start_time.slice(0,5)+'-'+pre_str.end_time.slice(0,5));
                if(i === backData.length-1)
                    this.createShow(templist);
            }
            
        }
        lastWeekday = this.weekday;
      }
    },
    
    // 获取用户和医生的初始化信息
    obtainUserDetails() {
      getSingleUser(this.userid).then
      (response => 
        {
          if(response.status === 200) {
            this.username = response.data.username;
            this.email = response.data.email;
            this.avatar = response.data.avatar;
          }
        }
      ).catch
      (error =>
        {
          console.error('Enquiry Failed.', error);
          this.$message.error('查询用户详情时发生网络错误，请检查网络状况！');
        }
      )
    },

    obtainDoctorDetails() {
      getSingleDoctor(this.doctor_id).then
      (response =>
        {
          if(response.status === 200) {
            this.name = response.data.real_name;
            this.idno = response.data.ID_number;
            this.tel = response.data.phone_number;
            this.appoiOpen = response.data.is_service;
            this.obtainAvailableTime();
          }
        }
      ).catch
      (error =>
        {
          console.error('Enquiry Failed.', error);
          this.$message.error(`查询医生详情时发生网络错误，请检查网络状况！`);
        }
      )
    },

    // 保存用户的患者信息,发送到后端
    confirmInfo(name, idno, tel){
      createNewPatient(name, idno, tel).then
      (response =>
        {
          if(response.status === 201) {
            // for debug
            this.$message.success(`成功创建患者信息！patient_id为${response.data.id}`);
          }
        }
      ).catch
      (error =>
        {
          if(error.response) {
            if(error.response.status === 401) {
              console.error('Unauthorized.', error);
              // for debug
              this.$message.error('很抱歉，您暂未登录，无法使用预约功能！');
              return;
            }
          }
          console.error('Fail to Create New Patient.', error);
          this.$message.error('创建患者信息时发生网络错误，请检查网络状况！');
        }
      )
      // for debug
      console.log(`${name}`)
      console.log(`${idno}`)
      console.log(`${tel}`)
    },

    // 获取原先的医生信息
    obtainOriginDoctorDetails() {
      if(this.doctor_id) {
        getSingleDoctor(this.doctor_id).then
        (response =>
          {
            if(response.status === 200) {
              this.doctor_origin = response.data;
            }
          }
        ).catch
        (error =>
          {
            console.error('Enquiry Failed.', error);
            this.$message.error('查询医生详细信息时发生网络错误，请检查网络状况！');
          }
        )
      }
      else {
        // for debug
        console.error('并非医生！');
      }
    },

    // 医生个人中心页面中的按钮：已提交接诊时间情况下，关闭了接诊
    switchStatus(){
      if(this.init){
       if(!this.appoiOpen)
       {
          // 清空显示界面
          this.clearShow()
          this.init = false
          // 1. 设置后端is_service = false
          updateDoctor(
            this.doctor_id, 
            this.doctor_origin.certificate_image_url, 
            this.doctor_origin.real_image_url,
            this.doctor_origin.phone_number,
            false,
            this.doctor_origin.description).then
            (response =>
              {
                if(response.status === 200) {
                  // for debug
                  this.$message.success(`关闭接诊状态成功！`);
                }
              }
            ).catch
            (error =>
              {
                if(error.response) {
                  if(error.response.status === 401) {
                    console.error('Unauthorized.', error);
                    // for debug
                    this.$message.error('很抱歉，您暂未登录，无法修改自己的接诊状态！');
                    return;
                  }
                }
                console.error('Fail to Change Service Status.', error);
                this.$message.error('更改接诊状态时发生网络错误，请检查网络状况！');
              }
            )
          //
          // 2. 使用api DELETE 清空接诊时间
          abortDoctorTimetable(this.doctor_id);
          //
       } 
      }
    },

    // 未开启接诊的医生确认提交接诊信息 datasend为列表 每一条记录为json 对应e_CutePet的api要求
    confirmAppoint(){
      //首先修改后端医生的is_service信息为true
      //this.$message(`${this.doctor_origin.real_image_url}`);
      updateDoctor(
        this.doctor_id, 
        '', 
        this.doctor_origin.real_image_url,
        this.doctor_origin.phone_number,
        true,
        this.doctor_origin.description).then
        (response =>
          {
            if(response.status === 200) {
              // for debug
              this.$message.success(`打开接诊状态成功！`);
            }
          }
        ).catch
        (error =>
          {
            if(error.response) {
              if(error.response.status === 401) {
                console.error('Unauthorized.', error);
                // for debug
                this.$message.error('很抱歉，您暂未登录，无法修改自己的接诊状态！');
                return;
              }
            }
            console.error('Fail to Change Service Status.', error);
            this.$message.error('更改接诊状态时发生网络错误，请检查网络状况！');
          }
        )
      //
      // 然后利用dataSend把接诊数据发给后端
      const dataSend = this.front2back(this.preData)

      for(var i = 0; i < dataSend.length; i++) {
        createNewTimetable_doctor(
          dataSend[i].day_of_week,
          dataSend[i].start_time,
          dataSend[i].end_time).then
          (response =>
            {
              if(response.status === 201) {
                // for debug
                console.log(`成功新建一条可用接诊时间，在dataSend中的序号为${i}`);
              }
            }
          ).catch
          (error =>
            {
              if(error.response) {
                if(error.response.status === 401) {
                  console.error('Unauthorized.', error);
                  // for debug
                  this.$message.error('很抱歉，您暂未登录，无法新增接诊记录！');
                  return;
                }
              }
              console.error(`Fail to Create New piece of Timetable.ID in dataSend: ${i}`, error);
              this.$message.error('新建可预约时间时发生网络错误，请检查网络状况！');
            }
          )
      }
      
      this.init = true
    },

    // 获取医生可接诊时间
    obtainAvailableTime() {
      console.log(`${this.appoiOpen}`);
      if(this.appoiOpen) {
        getDoctorTimetable(this.doctor_id, null, null, null, null, 'day_of_week,start_time', 1, 199).then
        (response =>
          {
            if(response.status === 200) {
              this.openTime = response.data.results;
              // for debug
              const dayOfWeekType = typeof response.data.results[0].day_of_week;  
              console.log(`Day of week type: ${dayOfWeekType}`);  
              console.log(`${response.data.results[0].day_of_week}`);
              console.log(`${response.data.results[0].day_of_week}`);
              this.back2front(this.openTime);
            }
          }
        ).catch
        (error =>
          {
            if(error.response) {
              if(error.response.status === 401) {
                console.error('Unauthorized.', error);
                // for debug
                this.$message.error('很抱歉，您暂未登录，无法查询医生预约时间列表！');
                return;
              }
            }
            console.error('Enquiry Failed.', error);
            this.$message.error('查询医生预约列表时发生网络错误，请检查网络状况！');
          }
        )
      }
      this.init = this.appoiOpen;
    },
  },
  computed:{
    isDoctor(){
      // 判断用户身份为患者/医生
      if(this.doctor_id) {
        return true;
      }
      else {
        return false;
      }
    },
    isOK(){
      if(this.name !== '' &&
         this.idno !== '' &&
         this.tel  !== '')
        return true
      else
        return false
    }
  },
  mounted() {
  
  },
  created() {
    const {id} = this.$route.params
    this.userid = id

    this.doctor_id = Cookies.get(`doctor_id`);

    this.obtainOriginDoctorDetails();

    // 如果用户是患者 只需获取用户名和email 
    if(!this.isDoctor)
    {
      this.obtainUserDetails();
    }
    // 如果用户是医生 还需要获取在注册时就填写了的name idno tel 以及 接诊时间信息
    else
    {
      this.obtainUserDetails();
      this.obtainDoctorDetails();
        // this.username = '清秋自有梧桐在'
        // this.email = '2479661334@qq.com'
        // this.avatar = this.avatar_default
        // this.name = '王梓健'
        // this.idno = '11451401010101'
        // this.tel = '19999999999'
        // this.appoiOpen = true;
      //this.obtainAvailableTime();
        // 根据is_service判断是否接诊
        // 否：appoiOpen = false
        // 是：appoiOpen = true 查询接诊时间 将其赋值给openTime 再将openTime加载到界面
        // 无论appoiOpen = true/false,都在此处将其复制一份给this.init用于显示界面
        // 将下面内容取消注释 演示处于接诊状态的医生
        // this.appoiOpen = true;
        // this.openTime = [
        //     {
        //         "id": "0",
        //         "day_of_week": 'DayofWeekEnum.星期二',
        //         "start_time": "11:00:00",
        //         "end_time": "14:00:00"
        //     },
        //     {
        //         "id": "0",
        //         "day_of_week": 'DayofWeekEnum.星期二',
        //         "start_time": "23:00:00",
        //         "end_time": "23:59:59"
        //     },
        //     {
        //         "id": "0",
        //         "day_of_week": 'DayofWeekEnum.星期四',
        //         "start_time": "08:00:00",
        //         "end_time": "10:00:00"
        //     },
        //     {
        //         "id": "0",
        //         "day_of_week": 'DayofWeekEnum.星期日',
        //         "start_time": "12:00:00",
        //         "end_time": "13:00:00"
        //     },
        // ]
        // //将openTime数据加载到界面内
        // this.back2front(this.openTime);
    }
  },
  }
</script>
  
<style scoped>
.infoWindow{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.info_bg{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  margin-bottom: 30px;
  padding: 0px;
  height: 854px;
  width: 958px;
  background-image: url("../assets/images/home/myinfo_list.png");
}

.info_bg2{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  margin-bottom: 30px;
  padding: 0px;
  height: 1380px;
  width: 958px;
  background-image: url("../assets/images/home/myinfo_list2.png");
}

.info_details{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  padding: 0px;
  height: 790px;
  width: 930px;
  margin-left: 15px;
  margin-top: 50px;
}

.info_details2{
  display: flex;
  flex-direction: column;
  justify-content: start; 
  padding: 0px;
  height: 1380px;
  width: 930px;
  margin-left: 15px;
  margin-top: 50px;
}

.tableContainer >>> .el-table .cell {
  white-space: pre-line;
}

.tip_info{
  text-align: left;
  margin-top: 25px;
  margin-left: 15px;
  margin-bottom: 0px;
  color: #A68879;
  font-size: 14px;
}

.img_info{
  display: flex;
  flex-direction: row;
  width: 890px;
  height: 110px;
  margin-left: 20px;
  margin-bottom: 0px;
  margin-top: 40px;
}

.img_info p{
  width: 60px;
  margin-top: 10px;
  margin-left: 0px;
}

.img_info img{
  width: 105px;
  height: 105px;
  margin-left: 50px;
}

.img_info input{
  margin-left: 20px;
  height: 30px;
  margin-top: 80px;
}

.info_details>>>.el-textarea__inner {
  border: 0;
  resize: none;
  background-color: transparent;
}

.info_details2>>>.el-textarea__inner {
  border: 0;
  resize: none;
  background-color: transparent;
}

.username_info{
  display: flex;
  flex-direction: row;
  width: 890px;
  height: 50px;
  margin-left: 20px;
  margin-bottom: 0px;
  margin-top: 40px;
}

.username_info p{
  width: 60px;
  margin-top: 10px;
  margin-left: 6px;
}

.username_input{
  width: 350px;
  height: 25px;
  border: 1px solid #eeeeee;
  padding-bottom: 10px;
  font-size: 16px;
  margin-left: 40px;
  margin-top: 3px;
}

.email_info{
  display: flex;
  flex-direction: row;
  width: 890px;
  height: 50px;
  margin-left: 20px;
  margin-bottom: 0px;
  margin-top: 40px;
}

.email_info p{
  width: 60px;
  margin-top: 10px;
  margin-left: 0px;
}

.email_input{
  width: 350px;
  height: 25px;
  border: 1px solid #eeeeee;
  padding-bottom: 10px;
  font-size: 16px;
  margin-left: 45px;
  margin-top: 3px;
}

.wrap-text {
  white-space: pre-line;
  overflow-y: auto;
}

.addOpenButtons{
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  margin-left: 25px;  
}

.addOpenButtons .el-button{
  width: 120px;
  font-size: 12px;
  padding: 9px;
  margin-right: -10px;
  background-color: #e55e5e;
  border-color: #e55e5e;
  border-radius: 0px;
}

.timeTransfer{
  text-align: left;
  padding-left: 40px;
}

.timeConfirm{
  margin-left: 10px;
  padding: 6px 5px;
  width: 80px;
  background-color: #e55e5e;
  color: white;
  border-color: #e55e5e;
}

.timeTransfer>>>.el-transfer__button {
  background-color: #e55e5e;
  border-color: #e55e5e;
}

.controlOpenButtons{
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  margin-left: 25px;
  margin-top: 30px;  
}

.controlOpenButtons .el-button{
  background-color: #FFA500;
  border-color: #FFA500;
}

.doctorTip{
  font-size: 11px;
  margin-left: 30px;
  margin-top: -20px;
}

.doctorTip h3{
  text-align: left;
}

.doctorTip p{
  text-align: left;
}

</style>
  