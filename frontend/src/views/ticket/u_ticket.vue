<template>
  <div class="app-container">
    <div class="ticket">
      <div class="ticket-form" v-if="customfield_list.length > 0">
        <el-form ref="temp" :model="temp" label-width="100px">
          <el-card>
            <div slot="header" class="card-solt">
              <el-form-item label="工單標題">
                <el-input v-model="ticket.name" />
              </el-form-item>
            </div>
            <el-row :gutter="20">
              <el-col
                :md="{
                  span: [7, 8, 9, 12].includes(item.field_type) ? 22 : 11,
                }"
                v-for="item in customfield_list"
                :key="item.id"
              >
                <el-form-item
                  v-show="!item.field_attribute"
                  :label="item.field_name"
                  :prop="item.field_key"
                  :rules="
                    match_fields.includes(item.id) && item.field_type !== 15
                      ? [
                          {
                            required: true,
                            message: '請輸入' + item.field_name,
                            trigger: 'blur',
                          },
                        ]
                      : []
                  "
                >
                  <el-input
                    v-if="item.field_type === 1"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  />

                  <el-input-number
                    v-if="item.field_type === 2"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  ></el-input-number>

                  <el-date-picker
                    type="date"
                    v-if="item.field_type === 5"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  ></el-date-picker>

                  <el-date-picker
                    type="datetime"
                    v-if="item.field_type === 6"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  ></el-date-picker>

                  <el-input
                    type="textarea"
                    :autosize="{ minRows: 4, maxRows: 6 }"
                    v-if="item.field_type === 8"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  ></el-input>

                  <el-switch
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    v-if="item.field_type === 4"
                    v-model="temp[item.field_key]"
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  ></el-switch>

                  <el-radio-group
                    v-if="item.field_type === 9"
                    v-model="temp[item.field_key]"
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  >
                    <el-radio
                      v-for="(value, index) in JSON.parse(item.field_choice)"
                      :key="index"
                      :label="index"
                      >{{ value }}</el-radio
                    >
                  </el-radio-group>

                  <el-checkbox-group
                    v-if="item.field_type === 12"
                    v-model="temp[item.field_key]"
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  >
                    <el-checkbox
                      v-for="(value, index) in JSON.parse(item.field_choice)"
                      :key="index"
                      :label="index"
                      >{{ value }}</el-checkbox
                    >
                  </el-checkbox-group>

                  <el-select
                    v-if="item.field_type === 10"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    clearable
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  >
                    <el-option
                      v-for="(value, index) in JSON.parse(item.field_choice)"
                      :key="index"
                      :value="index"
                      >{{ value }}</el-option
                    >
                  </el-select>

                  <el-select
                    v-if="item.field_type === 13"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    clearable
                    multiple
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  >
                    <el-option
                      v-for="(value, index) in JSON.parse(item.field_choice)"
                      :key="index"
                      :value="index"
                      >{{ value }}</el-option
                    >
                  </el-select>

                  <el-date-picker
                    v-if="item.field_type === 7"
                    v-model="temp[item.field_key]"
                    format="yyyy 年 MM 月 dd 日"
                    value-format="yyyy-MM-dd"
                    type="daterange"
                    range-separator="至"
                    start-placeholder="開始日期"
                    end-placeholder="結束日期"
                  ></el-date-picker>

                  <el-select
                    v-if="item.field_type === 11"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    clearable
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  >
                    <el-option
                      v-for="t in user_list"
                      :key="t.id"
                      :label="t.username"
                      :value="t.username"
                    ></el-option>
                  </el-select>

                  <el-select
                    v-if="item.field_type === 14"
                    v-model="temp[item.field_key]"
                    :placeholder="item.field_name"
                    clearable
                    multiple
                    :disabled="
                      item.field_attribute || !match_fields.includes(item.id)
                    "
                  >
                    <el-option
                      v-for="t in user_list"
                      :key="t.id"
                      :label="t.username"
                      :value="t.username"
                    ></el-option>
                  </el-select>

                  <el-upload
                    v-if="item.field_type === 15"
                    action="/api/tool/upload/"
                    :headers="uploadHeaders"
                    :on-preview="handlePreview"
                    :on-remove="handleRemove"
                    :file-list="fileList"
                    :data="{ username: username }" 
                    :disabled="item.field_attribute || !match_fields.includes(item.id)"
                    accept=".pdf"
                    :on-success="handleUploadSuccess"
                  >
                    <el-button slot="trigger" type="primary">選擇檔案</el-button>
                    <div slot="tip" class="el-upload__tip">只能上傳pdf文件</div>
                  </el-upload>

                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item>
              <span
                style="margin: 0 5px"
                v-for="item in transition_list"
                :key="item.id"
              >
                <el-button
                  v-if="item.name === 1"
                  :type="btn_types[item.name]"
                  @click="selectUser('temp', item)"
                  >{{ item.name | TransitionNameFilter }}</el-button
                >
                <el-button
                  v-else
                  :type="btn_types[item.name]"
                  @click="handleSave('temp', item)"
                  >{{ item.name | TransitionNameFilter }}</el-button
                >
              </span>
            </el-form-item>
          </el-card>
        </el-form>
      </div>
      <div v-else>
        <h1 style="text-align: center">沒有設定工作流程字段</h1>
      </div>
    </div>

    <el-dialog :visible.sync="dialogVisible">
      <div slot="title">
        目前下一步處理對象是：
        <a style="color: red; font-size: 24px">{{
          participant_type[dialogChooiceType]
        }}</a>
        <span v-if="dialogChooiceType==='none'">請直接點確定</span>
        <span v-else>請點選下方處理對象，選擇轉交用戶</span>
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-collapse
            v-model="dialogChooiceType"
            accordion
            @change="selectType"
          >
            <el-collapse-item title="用戶" name="user" disabled></el-collapse-item>
            <el-collapse-item title="部門" name="group" disabled>
              <div v-if="group_role_list.length > 0">
                <li v-for="item in group_role_list" :key="item.id">
                  <el-button
                    style="margin: 2px"
                    size="mini"
                    plain
                    @click="checkGroupUser(item.id)"
                  >
                    {{ item.name }}
                  </el-button>
                </li>
              </div>
              <div v-else>
                没有可选{{ participant_type[dialogChooiceType] }}
              </div>
            </el-collapse-item>
            <el-collapse-item title="角色" name="role" disabled>
              <div v-if="group_role_list.length > 0">
                <li v-for="item in group_role_list" :key="item.id">
                  <el-button
                    style="margin: 2px"
                    size="mini"
                    plain
                    @click="checkRoleUser(item.id)"
                  >
                    {{ item.name }}
                  </el-button>
                </li>
              </div>
              <div v-else>
                沒有可選{{ participant_type[dialogChooiceType] }}
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-col>
        <el-col :span="16">
          <el-table
            :data="choice_user_list"
            @row-click="checkTableUser"
            style="width: 100%"
          >
            <el-table-column
              prop="username"
              label="用戶"
              width="180"
            ></el-table-column>
            <el-table-column prop="realname" label="姓名"></el-table-column>
          </el-table>
        </el-col>
      </el-row>

      <el-row>
        <el-input readonly v-model="ticket.participant">
          <template slot="prepend">選擇用戶</template>
        </el-input>
      </el-row>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button
          :disabled="ticket.participant ? false : true"
          type="primary"
          @click="handleButton('temp', choice_transition)"
          >確 定</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {
  workflow,
  customfield,
  state,
  transition,
  ticket,
  user,
  auth,
} from "@/api/all";

import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";
import { mapGetters } from "vuex";
import { GenDatetime } from "@/utils";
import { getToken } from '@/utils/auth'

export default {
  name: "u_ticket",

  components: {},
  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false,
      },
      tempRoute: {},
      wfdata: {},
      customfield_list: [],
      state_list: [],
      transition_list: [],
      user_list: [],
      temp: {},
      rules: {},
      btn_types: {
        0: "primary",
        1: "success",
        2: "warning",
        3: "danger",
      },
      match_fields: [],
      ticket: {
        name: "",
        participant: "",
      },
      workflow_temp: {
        participant: this.user_id,
      },
      choice_user_list: [],
      dialogChooiceType: "none",
      dialogVisible: false,
      participant_list: [],
      choice_transition: {},
      group_role_list: [],
      participant_type: {
        "none": "無處理人",
        "user": "個人",
        "group": "部門",
        "role": "角色",
      },
      fileList: [], // Added for file upload
    };
  },
  computed: {
    ...mapGetters(["username", "user_id"]),
    uploadHeaders() {
      const token = this.getAuthToken();
      console.log("Retrieved token:", token); // Log the token
      return {
        Authorization: `core ${token || ''}`, // Provide a fallback value
      };
    },
  },
  created() {
    const id = this.$route.params && this.$route.params.id;
    this.fetchData(id);
    this.getUserList();
    this.tempRoute = Object.assign({}, this.$route);
  },
  methods: {
    fetchData(id) {
      this.workflow_temp.workflow = id;
      const params = {
        id: id,
      };
      workflow.requestGet(params).then((response) => {
        this.wfdata = response.results[0];
        this.setPageTitle();

        const d = new Date();
        this.ticket.name = this.wfdata.name + "-" + GenDatetime(d);
        this.getCustomfieldList();
        this.getStateList();
      });
    },
    getCustomfieldList() {
      customfield.requestGet(this.workflow_temp).then((response) => {
        this.customfield_list = response.results;
      });
    },
    getStateList(id) {
      state.requestGet(this.workflow_temp).then((response) => {
        this.state_list = response.results;
        this.match_fields = this.state_list[1].fields;
        this.getTransitionList(this.state_list[0].id);
      });
    },
    getTransitionList(source_state) {
      this.workflow_temp.source_state = source_state;
      transition.requestGet(this.workflow_temp).then((response) => {
        this.transition_list = response.results;
      });
    },
    getUserList() {
      user.requestGet().then((response) => {
        this.user_list = response.results;
      });
    },
    handleFilter() {
      this.fetchData();
    },
    setPageTitle() {
      const title = this.wfdata.name;
      document.title = `${title} - 創建`;
    },
    selectUser(dataForm, row) {
      this.$refs[dataForm].validate((valid) => {
        if (valid) {
          this.dialogVisible = true;
          this.choice_transition = row;
          this.dialogChooiceType = row.dest_state.participant_type;
          this.selectType(this.dialogChooiceType);
        }
      });
    },
    selectType(val) {
      if (val === 'user') {
        this.choice_user_list = this.choice_transition.dest_state.user_participant;
      } else if (val == 'group') {
        this.group_role_list = this.choice_transition.dest_state.group_participant;
      } else if (val == 'role') {
        this.group_role_list = this.choice_transition.dest_state.role_participant;
      } else {
        this.ticket.participant = this.username
      }
    },
    checkGroupUser(id) {
      const params = {
        group: id,
      };
      user.requestGet(params).then((response) => {
        this.choice_user_list = response.results;
      });
    },
    checkRoleUser(id) {
      const params = {
        roles: id,
      };
      user.requestGet(params).then((response) => {
        this.choice_user_list = response.results;
      });
    },
    checkTableUser(row) {
      this.ticket.participant = row.username;
    },
    handleSave(dataForm, transition) {
      this.ticket.participant = this.username;
      this.handleButton(dataForm, transition);
    },
    handleButton(dataForm, transition) {
      this.dialogVisible = false;
      const customfield = [];
      for (var i of this.customfield_list) {
        if (this.temp[i.field_key]) {
          customfield.push({
            customfield: i.id,
            field_key: i.field_key,
            field_value: this.temp[i.field_key],
          });
        } else {
          customfield.push({
            customfield: i.id,
            field_key: i.field_key,
            field_value: "",
          });
        }
      }
      const data = Object.assign(
        {},
        {
          name: this.ticket.name,
          participant: this.ticket.participant,
          create_user: this.user_id,
          workflow: this.wfdata.id,
          state: transition.dest_state.id,
          transition: transition.id,
          customfield: JSON.stringify(customfield),
          relation: this.ticket.participant,
        }
      );
          ticket
            .requestPost(data)
            .then((res) => {
              this.$notify({
                title: "成功",
                message: "創建成功",
                type: "success",
                duration: 2000,
              });
              this.$router.push({ path: "/my_ticket" });
            })
            .catch(e => {
              console.log(e)
            });
    },
    handlePreview(file) {
      console.log(file);
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    getAuthToken() {
      return getToken(); // This is assuming you have a method to get the token
    },
    handleUploadSuccess(response, file, fileList) {
      if (response.code === 20000 && response.results) {
        const serverFileName = response.results.filename;
        let fileUrl = response.results.file;
        
        // Replace localhost or 127.0.0.1 with the server's IP
        const serverIP = 'websystem.life'; // Your server's actual IP
        const localhost = '0.0.0.0'
        var ipRegex = new RegExp('\b' + localhost + '\b');
        var newUrl = originalUrl.replace(ipRegex, serverIP);

        // Extract original file name
        const originalFileName = file.name || serverFileName.split('-')[0] + '.pdf';

        this.$store.dispatch('fileUpload/setUploadedFileInfo', {
          name: originalFileName,
          url: newUrl
        });

        this.$message.success('File uploaded successfully');
      } else {
        this.$message.error('File upload failed');
        console.error('Upload failed:', response);
      }
    },
  }
};
</script>
