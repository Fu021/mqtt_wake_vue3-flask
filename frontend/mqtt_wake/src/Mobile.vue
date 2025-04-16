<script setup>
import { ref, computed } from "vue";
import axios from 'axios'
import api_url from "@/api_url.js";

const alive_color = 'rgb(80,255,80)'
const not_alive_color = 'rgb(255,80,80)'

const dialogVisible = ref(false)
const dialog_title = ref("")
const dialog_content = ref("")
const active_index = ref('1')
const device_info = ref([])
const newDevice = ref({
  id: '',
  name: ''
})

get_info()

const check_timer = setInterval(() => {
  get_info()
}, 5000);

function handleSelect(index) {
  active_index.value = index
  newDevice.value = {'id':'','name':''}
}

function handleDelete(id) {
  axios.post(api_url + '/api/delete',{'id':id})
  .then(res => {
    if (res.data.msg === -1)
    {
      dialog_title.value = "错误"
      dialog_content.value = "设备不存在，请刷新页面后重试"
      dialogVisible.value = true
      get_info()
    }
    else
    {
      dialog_title.value = "提示"
      dialog_content.value = "设备删除成功"
      dialogVisible.value = true
      get_info()
    }
  })
}

function handleAdd() {
  const id = Number(newDevice.value.id)
  const name = newDevice.value.name

  if (isNaN(id)) {
    dialog_title.value = "错误"
    dialog_content.value = "设备id应当是一个整数"
    dialogVisible.value = true
    return;
  }

  axios.post(api_url + '/api/add',{'id':id,'name':name})
  .then(res => {
    if (res.data.msg === 1)
    {
      dialog_title.value = "提示"
      dialog_content.value = "设备新建成功"
      dialogVisible.value = true
      get_info()
    }
    else if (res.data.msg === -1)
    {
      dialog_title.value = "错误"
      dialog_content.value = "请检查设备id是否为不小于0的整数，设备名称是否为非空字符串"
      dialogVisible.value = true
    }
    else
    {
      dialog_title.value = "错误"
      dialog_content.value = "设备id重复"
      dialogVisible.value = true
    }
  })
}

function check(id) {
  axios.post(api_url + '/api/check_alive',{'id':id})
  .then(res => {
    if (res.data.msg === -1)
    {
      dialog_title.value = "错误"
      dialog_content.value = "设备不存在，请刷新页面后重试"
      dialogVisible.value = true
      get_info()
      return
    }

    const target = device_info.value.find(device => device.id === id)
    target.alive = res.data.msg
  })
}

function wake(id) {
  axios.post(api_url + '/api/wake',{'id':id})
}

function get_info() {
  axios.get(api_url + '/api/get_info')
  .then(res => {
    device_info.value = res.data
  })
}

</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialog_title"
    width="300"
  >
    <span>{{ dialog_content }}</span>
    <template #footer>
      <div>
        <el-button @click="dialogVisible = false">确认</el-button>
      </div>
    </template>
  </el-dialog>

  <el-row>
      <el-col :span="24">
        <el-menu
          default-active="2"
          mode="horizontal"
          style="margin-top: 1vh;"
        >
        </el-menu>
      </el-col>
  </el-row>
  <el-row>
    <el-col :span="24" v-if="active_index === '1'">
      <el-row v-for="(device,index) in device_info" :key="index">
        <el-divider v-if="index === 0" style="margin-top: 0;"/>
          <el-col :span="8" :push="2">
              <div style="display: flex; align-items: center;">
                  <div style="width: 15px; height: 15px; border-radius: 50%;" 
                  :style="{ backgroundColor: device.alive ? alive_color : not_alive_color }"></div>
                  <el-text size="large" style="margin-left: 5px;">{{ device.name }}</el-text>
              </div>
          </el-col>
          <el-col :span="8" :push="2">
              <el-button @click="check(device.id)">查询在线状态</el-button>
          </el-col>
              <el-col :span="8" :push="0">
              <el-button @click="wake(device.id)">远程唤醒设备</el-button>
          </el-col>
        <el-divider />
      </el-row>
    </el-col>
    
      <!-- 设备管理 -->
    <el-col :span="24" v-if="active_index === '2'">
      <div style="margin-left: 5vw;margin-top: 3vh;margin-bottom: 3vh;">
        <el-text size="large">全部设备</el-text>
      </div>

      <div style="width: 100%; display: flex; justify-content: center;">
        <el-table :data="device_info" 
        style="margin-bottom: 3vw;width: 360px;">
          <el-table-column prop="name" label="设备名称" width="120" />
          <el-table-column prop="id" label="设备 ID" width="120" />
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button
                type="danger"
                size="small"
                @click="handleDelete(scope.row.id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div style="margin-left: 5vw;margin-top: 3vh;margin-bottom: 3vh;">
        <el-text size="large">新增设备</el-text>
      </div>

      <el-form :inline="true" :model="newDevice" style="margin-top: 3vh;">
        <el-row justify="center">
          <el-form-item label="设备名称">
            <el-input v-model="newDevice.name" placeholder="请输入名称" style="width:30vw"/>
          </el-form-item>
        </el-row>
        <el-row justify="center">
          <el-form-item label="设备 ID">
            <el-input v-model="newDevice.id" placeholder="请输入ID" style="width:30vw"/>
          </el-form-item>
        </el-row>
        <el-row justify="center">
          <el-form-item>
            <el-button type="primary" @click="handleAdd" style="width:50vw">提交</el-button>
          </el-form-item>
        </el-row>
      </el-form>
    </el-col>
  </el-row>
    <el-row>
      <el-col :span="24">
        <el-menu
        default-active="1"
        @select="handleSelect"
        style="position: fixed; bottom: 0; height: 10vh; display: flex; justify-content: space-evenly; width: 100%; padding: 0; margin: 0;"
        mode="horizontal"
        >
        <el-menu-item index="1" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <span>远程唤醒</span>
        </el-menu-item>
        <el-menu-item index="2" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <span>设备管理</span>
        </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
</template>