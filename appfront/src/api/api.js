// appfront/src/api/api.js
import axiosInstance from './index'
import Cookies from 'js-cookie'

const axios = axiosInstance

// 忽略的功能（但后端提供了支持的API）：
// 1. 商城板块：更新/修改商品评论
// 2. 社区板块：
//      （1）更新/修改帖子内容
//      （2）更新/修改帖子评论
//      


//登录界面
export const login = (username, passwd) => {  
    return axios.post(`http://182.92.171.51:8000/api/auth/login`, {  
      'username': username,  
      'password': passwd  
    }); 
}

//注册界面
export const verifyEmail = (user_email) => {
    const params = {
        'email':user_email
    }
    return axios.post(`http://182.92.171.51:8000/api/verify_email/register`, params );
}

export const normRegister = (username, email, passwd, verify_code) => {  
return axios.post(`http://182.92.171.51:8000/api/users/register`, {  
    "username":username,
    "email":email,
    "password":passwd,
    "verify_code":verify_code,
});  
}

export const DocRegister = (username, email, passwd, id, name, cno, verify_code) => {  
    return axios.post(`http://182.92.171.51:8000/api/doctors/register`, {
        "user":{
            "password": passwd,
            "username": username,
            "email": email,
            "verify_code": verify_code
        },
        "ID_number": id, 
        "real_name": name, 
        "certificate_number": cno
    });  
}

// 商城板块
export const getGoodList = (
    key_word,
    category,
    parent_category,
    is_hot = false, 
    is_new = false, 
    ordering = 'create_time,sold_num,price', 
    page = 1, 
    page_size = 10
) => {
    const params = {
        "search": key_word,
        "category": category,
        "parent_category": parent_category,
        "is_hot": is_hot,
        "is_new": is_new,
        "ordering": ordering,
        "page": page,
        "page_size": page_size
    };
    return axios.get(`http://182.92.171.51:8000/api/shop/goods`, { params: params });
}

export const getSingleGood = (good_id) => {
    return axios.get(`http://182.92.171.51:8000/api/shop/goods/${good_id}`);
}

export const favorGood = (good_id) => {
    const token = Cookies.get('token');  
    const headers = token ? {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
    } : {};
    if (!headers['Content-Type']) {  
        headers['Content-Type'] = 'application/json';  
    }
    return axios.put(`http://182.92.171.51:8000/api/shop/goods/favor/${good_id}`, null, { headers: headers });
}

export const getFavorGoodList = (
    key_word = '',
    category,
    parent_category,
    is_hot, 
    is_new, 
    ordering = 'create_time,sold_num,price', 
    page = 1, 
    page_size = 10
) => {
    const params = {
        "good_name": key_word,
        "good_category": category,
        "good_parent_category": parent_category,
        "is_hot": is_hot,
        "is_new": is_new,
        "ordering": ordering,
        "page": page,
        "page_size": page_size
    };
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.get(`http://182.92.171.51:8000/api/shop/goods/favor`, {
        params: params,
        headers: headers
    });
}

export const getCategory_1 = (good_category_id) => {
    return axios.get(`http://182.92.171.51:8000/api/shop/goods/category/Level1/${good_category_id}`);
}

export const getCategory_2 = (good_category_id) => {
    return axios,get(`http://182.92.171.51:8000/api/shop/goods/category/Level2/${good_category_id}`);
}

export const createNewOrder = (good_id, address, user_name, phone_number) => {
    const data = {
        "address": address,
        "signer_name": user_name,
        "signer_mobile": phone_number
    };
    const token = Cookies.get('token');
    const config = {  
        headers: token ? {  
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`  
        } : {}  
    };
    // const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.post(`http://182.92.171.51:8000/api/shop/trades/order/create/${good_id}`, data, config);
}

export const getOrdersList = (
    good_name = "",
    good_category_self = '',  // 二级标签名
    ordering = 'create_time,sold_num,price', 
    page = 1, 
    page_size = 10
    ) => {
    const params = {
        "good_name": good_name,
        "good_category_name": good_category_self,
        "ordering": ordering,
        "page": page,
        "page_size": page_size
    };
    const token = Cookies.get('token');
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.get(`http://182.92.171.51:8000/api/shop/trades/order`, {
        params: params,
        headers: headers
    });
}

export const getSingleOrder = (order_id) => {
    const token = Cookies.get('token');
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.get(`http://182.92.171.51:8000/api/shop/trades/order/${order_id}`, { headers: headers});
}

export const reviseOrder = (
    order_id,
    is_sign,
    address,
    signer_name,
    signer_mobile
    ) => {
    const data = {
        "is_sign": is_sign,
        "address": address,
        "signer_name": signer_name,
        "signer_mobile": signer_mobile
    }
    const token = Cookies.get('token');  
    const headers = token ? {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
    } : {};
    if (!headers['Content-Type']) {  
        headers['Content-Type'] = 'application/json';  
    }
    return axios.put(`http://182.92.171.51:8000/api/shop/trades/order/${order_id}`, data, { headers:headers });
}

export const deprecateOrder = (order_id) => {
    const token = Cookies.get('token');  
    const headers = token ? {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
    } : {};
    if (!headers['Content-Type']) {  
        headers['Content-Type'] = 'application/json';  
    }
    return axios.delete(`http://182.92.171.51:8000/api/shop/trades/order/${order_id}`, { headers: headers});
}

export const createNewGoodComment = (order_id, rating, content) => {
    const data = {
        "rating": rating,
        "content": content
    };
    const token = Cookies.get('token');
    const config = {  
        headers: token ? {  
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`  
        } : {}  
    };
    return axios.post(`http://182.92.171.51:8000/api/shop/trades/comment/create/${order_id}`, data, config);
}

export const getGoodCommentList = (
    good_id,
    good_name,
    good_category,
    rating,
    user_id,
    user_username,
    ordering = 'create_time,modify_time,rating',
    page = 1,
    page_size = 10,
) => {
    const params = {
        "good_id": good_id,
        "good_name": good_name,
        "good_category": good_category,
        "rating": rating,
        "user_id": user_id,
        "user_username": user_username,
        "ordering": ordering,
        "page": page,
        "page_size": page_size
    };
    return axios.get(`http://182.92.171.51:8000/api/shop/trades/comment`, { params: params });
}

export const getSingleGoodComment = (comment_id) => {
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.get(`http://182.92.171.51:8000/api/shop/trades/comment/${comment_id}`, { headers: headers });
}

export const deprecateGoodComment = (comment_id) => {
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.delete(`http://182.92.171.51:8000/api/shop/trades/comment/delete/${comment_id}`, { headers: headers });
}

// 社区板块
export const getPostsList = (
    key_word,
    post_author,
    tag,
    is_hot,
    is_new,
    ordering = 'create_time,click_num,favor_num,comment_num',
    page = 1,
    page_size = 10
) => {
    const params = {
        "search": key_word,
        "author": post_author,
        "tag": tag,
        "is_hot": is_hot,
        "is_new": is_new,
        "ordering": ordering,
        "page": page,
        "page_size": page_size
    };
    return axios.get(`http://182.92.171.51:8000/api/forum/posts`, { params: params});
}

export const getSinglePost = (post_id) => {
    return axios.get(`http://182.92.171.51:8000/api/forum/posts/${post_id}`);
}

export const createNewPost = (
    tag,
    title,
    brief_content,
    content,
) => {
    const data = {
        "tag_name": tag,
        "title": title,
        "brief_content": brief_content,
        "content": content,
    }
    const token = Cookies.get('token');
    const config = {  
        headers: token ? {  
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`  
        } : {}  
    };
    return axios.post(`http://182.92.171.51:8000/api/forum/posts/create/${tag}`, data, config);
}

export const deprecatePost = (post_id) => {
    const token = Cookies.get('token');  
    const headers = token ? {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
    } : {};
    if (!headers['Content-Type']) {  
        headers['Content-Type'] = 'application/json';  
    }
    return axios.delete(`http://182.92.171.51:8000/api/forum/posts/delete/${post_id}`, { headers: headers});
}

export const favorPost = (post_id) => {
    const token = Cookies.get('token');  
    const headers = token ? {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
    } : {};
    if (!headers['Content-Type']) {  
        headers['Content-Type'] = 'application/json';  
    }
    return axios.put(`http://182.92.171.51:8000/api/forum/posts/favor/${post_id}`, null, { headers: headers});
}

export const getFavorPostList = (
    ordering = 'create_time,post__favor_num,post__create_time,post__modify_time',
    page = 1,
    page_size = 10
) => {
    const params = {
        "ordering": ordering,
        "page": page,
        "page_size": page_size
    }
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.get(`http://182.92.171.51:8000/api/forum/posts/favor`, {
        params: params,
        headers: headers
    });
}

export const getPostCommentList = (
    post_id,
    user_id,
    user_username,
    ordering = 'create_time,modify_time',
    page = 1,
    page_size = 10
) => {
    const params = {
        "post_id": post_id,
        "user_id": user_id,
        "user_username": user_username,
        "ordering": ordering,
        "page": page,
        "page_size": page_size
    }
    return axios.get(`http://182.92.171.51:8000/api/forum/posts/comment`, { params: params });
}

export const createNewPostComment = (post_id, comment_text) => {
    const data = {
        "content": comment_text
    }
    const token = Cookies.get('token');  
    const config = {  
        headers: token ? {  
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`  
        } : {}  
    };
    return axios.post(`http://182.92.171.51:8000/api/forum/posts/comment/create/${post_id}`, data, config);
}

export const deprecatePostComment = (post_comment_id) => {
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.delete(`http://182.92.171.51:8000/api/forum/posts/comment/delete/${post_comment_id}`, { headers: headers });
}


// 个人中心 & 预约界面
export const updateUser = (user_id, avatar) => {
    const token = Cookies.get('token');
    const headers = token ? {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
    } : {};
    if (!headers['Content-Type']) {  
        headers['Content-Type'] = 'application/json';  
    }
    const data = {
        "avatar": avatar
    }
    return axios.put(`http://182.92.171.51/api/users/update/${user_id}`, data, { headers:headers });
}

export const getSingleUser = (user_id) => {
    return axios.get(`http://182.92.171.51:8000/api/users/${user_id}`);
}

export const updateDoctor = (
    doctor_id, 
    cert_pic, 
    real_pic, 
    phone_number, 
    is_service, 
    description) => {
        const data = {
            "certificate_image_url": cert_pic,
            "real_image_url": real_pic,
            "phone_number": phone_number,
            "is_service": is_service,
            "description": description
        }
        const token = Cookies.get('token');
        const headers = token ? {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        } : {};
        if (!headers['Content-Type']) {  
            headers['Content-Type'] = 'application/json';  
        }
        return axios.put(`http://182.92.171.51:8000/api/doctors/update/${doctor_id}`, data, { headers:headers });
}

export const getDoctorList = (
    ordering,
    page = 1,
    page_size = 10
) => {
    const params = {
        "ordering": ordering,
        "page": page,
        "page_size": page_size
    }
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.get(`http://182.92.171.51:8000/api/doctors`, {
        params: params,
        headers: headers
    });
}

export const getSingleDoctor = (doctor_id) => {
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.get(`http://182.92.171.51:8000/api/doctors/${doctor_id}`, { headers: headers });
}

export const createNewTimetable_doctor = (
    day,
    start_time,
    end_time
) => {
    const data = {
        "day_of_week": day,
        "start_time": start_time,
        "end_time": end_time
    }
    const token = Cookies.get('token');  
    const config = {  
        headers: token ? {  
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`  
        } : {}  
    };
    return axios.post(`http://182.92.171.51:8000/api/appointment/doctor/available_time/create`, data, config);
}

export const abortDoctorTimetable = (doctor_id) => {
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.delete(`http://182.92.171.51:8000/api/appointment/doctor/available_time/delete/${doctor_id}`, { headers: headers });
}

export const getDoctorTimetable = (
    doctor_id,
    begin_of_week,
    end_of_week,
    start_time,
    end_time,
    ordering,
    page,
    page_size
) => {
    const params = {
        "doctor_id": doctor_id,
        "begin_of_week": begin_of_week,
        "end_of_week": end_of_week,
        "start_time": start_time,
        "end_time": end_time,
        "ordering": ordering,
        "page": page,
        "page_size": page_size
    }
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.get(`http://182.92.171.51:8000/api/appointment/doctor/available_time`, {
        params: params,
        headers: headers
    });
}

export const createNewPatient = (
    real_name,
    ID_number,
    phone_number
) => {
    const data = {
        "real_name": real_name,
        "ID_number": ID_number,
        "phone_number": phone_number
    }
    const token = Cookies.get('token');  
    const config = {  
        headers: token ? {  
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`  
        } : {}  
    };
    return axios.post(`http://182.92.171.51:8000/api/appointment/patients/create`, data, config);
}

export const updatePatientDetails = (
    patient_id,
    real_name,
    ID_number,
    phone_number
) => {
    const data = {
        "real_name": real_name,
        "ID_number": ID_number,
        "phone_number": phone_number
    }
    const token = Cookies.get('token');  
    const headers = token ? {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
    } : {};
    if (!headers['Content-Type']) {  
        headers['Content-Type'] = 'application/json';  
    }
    return axios.put(`http://182.92.171.51:8000/api/appointment/patients/update/${patient_id}`, data, { headers:headers });
}

export const createNewAppointment = (
    doctor_id,
    appointment_time,
    pet_name,
    description
) => {
    const data = {
        "appointment_time": appointment_time,
        "pet_name": pet_name,
        "description": description
    }
    const token = Cookies.get('token');  
    const config = {  
        headers: token ? {  
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`  
        } : {}  
    };
    return axios.post(`http://182.92.171.51:8000/api/appointment/create/${doctor_id}`, data, config);
}

export const getAppointmentList = (
    status,
    doctor_id,
    patient_id,
    start_time,
    end_time,
    is_doctor,
    ordering,
    page,
    page_size
) => {
    const params = {
        "status": status,
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "start_time": start_time,
        "end_time": end_time,
        "is_doctor": is_doctor,
        "ordering": ordering,
        "page": page,
        "page_size": page_size
    }
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.get(`http://182.92.171.51:8000/api/appointment`, {
        params: params,
        headers: headers
    });
}

export const getSingleAppointment = (appointment_id) => {
    const token = Cookies.get('token');  
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    return axios.get(`http://182.92.171.51:8000/api/appointment/${appointment_id}`, { headers: headers });
}
