<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button-group>
        <el-button
          v-if="permissionList.add"
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleCreate"
          >{{ "添加" }}</el-button
        >
      </el-button-group>
    </div>

    <el-table :data="list" border style="width: 100%" highlight-current-row>
      <el-table-column label="名稱" prop="name">
        <template slot-scope="{ row }">
          <span>{{ row.name | TransitionNameFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="類型" prop="transition_type">
        <template slot-scope="{ row }">
          <span>{{ row.transition_type | TransitionTypeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="上一個節點" prop="source_state">
        <template slot-scope="{ row }">
          <span v-if="row.source_state">{{ row.source_state.name }}</span>
          <span v-else>None</span>
        </template>
      </el-table-column>
      <el-table-column label="下一個節點" prop="dest_state">
        <template slot-scope="{ row }">
          <span v-if="row.dest_state">{{ row.dest_state.name }}</span>
          <span v-else>None</span>
        </template>
      </el-table-column>
      <el-table-column label="屬性類型" prop="attribute_type">
        <template slot-scope="{ row }">
          <span>{{ row.attribute_type | AttributeTypeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        width="260"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              v-if="permissionList.update"
              size="small"
              type="primary"
              @click="handleUpdate(row)"
              >{{ "編輯" }}</el-button
            >
            <el-button
              v-if="permissionList.del"
              size="small"
              type="danger"
              @click="handleDelete(row)"
              >{{ "刪除" }}</el-button
            >
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      :title="textMap[dialogStatus]"
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
    >
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="100px"
        style="width: 400px; margin-left: 50px"
      >
        <el-form-item label="名稱" prop="name">
          <el-select v-model="temp.name" clearable placeholder="請選擇">
            <el-option
              v-for="(label, value) in transition_names"
              :key="value"
              :label="label"
              :value="parseInt(value)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="類型" prop="transition_type">
          <el-select
            v-model="temp.transition_type"
            clearable
            placeholder="請選擇"
          >
            <el-option
              v-for="(label, value) in transition_types"
              :key="value"
              :label="label"
              :value="parseInt(value)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="定時器" prop="timer">
          <el-input v-model="temp.timer" />‘
          <a class="tips"
            >流轉類型設置為定時器流轉時生效,單位秒。處於源狀態X秒後如果狀態都沒有過變化則自動流轉到目標狀態</a
          >
        </el-form-item>
        <el-form-item label="屬性類型" prop="attribute_type">
          <el-select
            v-model="temp.attribute_type"
            clearable
            placeholder="請選擇"
          >
            <el-option
              v-for="(label, value) in attribute_types"
              :key="value"
              :label="label"
              :value="parseInt(value)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上一個節點" prop="source_state">
          <el-select v-model="temp.source_state" clearable placeholder="請選擇">
            <el-option
              v-for="item in statedata"
              :key="item.id"
              :label="item.name"
              :value="parseInt(item.id)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="下一個節點" prop="dest_state">
          <el-select v-model="temp.dest_state" clearable placeholder="請選擇">
            <el-option
              v-for="item in statedata"
              :key="item.id"
              :label="item.name"
              :value="parseInt(item.id)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="條件表達式" prop="condition_expression">
          <el-input v-model="temp.condition_expression" />
        </el-form-item>
        <el-form-item label="點擊彈窗提示" prop="alert_enable">
          <el-switch
            v-model="temp.alert_enable"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </el-form-item>
        <el-form-item label="彈窗內容" prop="alert_text">
          <el-input v-model="temp.alert_text" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ "取消" }}</el-button>
        <el-button
          type="primary"
          @click="dialogStatus === 'create' ? createData() : updateData()"
          >{{ "確定" }}</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { transition, auth } from "@/api/all";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";

export default {
  name: "transition",
  props: {
    wfdata: {
      type: Object,
      default: {},
    },
    statedata: {
      type: Array,
      default: [],
    },
    list: {
      type: Array,
      default: [],
    },
  },
  components: {},
  data() {
    return {
      aaa: this.statedata,
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false,
      },
      temp: {},
      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "編輯",
        create: "添加",
      },
      rules: {
        name: [{ required: true, message: "請輸入名稱", trigger: "blur" }],
      },
      transition_types: {
        0: "常規流轉",
        1: "定時器流轉",
      },
      attribute_types: {
        0: "草稿",
        1: "待審",
        2: "駁回",
        3: "撤銷",
        4: "結束",
        5: "已關閉",
      },
      transition_names: {
        0: "保存",
        1: "轉交下一步",
        2: "駁回",
        3: "撤銷",
        4: "關閉",
      },
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
  },
  methods: {
    checkPermission() {
      this.permissionList.add = checkAuthAdd(this.operationList);
      this.permissionList.del = checkAuthDel(this.operationList);
      this.permissionList.view = checkAuthView(this.operationList);
      this.permissionList.update = checkAuthUpdate(this.operationList);
    },
    getMenuButton() {
      auth
        .requestMenuButton("transition")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    handleFilter() {},
    resetTemp() {
      this.temp = {
        memo: "",
        name: "",
        transition_type: 0,
        timer: 0,
        condition_expression: "[]",
        attribute_type: 0,
        alert_enable: false,
        alert_text: "",
        source_state: undefined,
        dest_state: undefined,
        workflow: this.wfdata.id,
      };
    },
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    createData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          this.temp.workflow = this.wfdata.id;
          transition
            .requestPost(this.temp)
            .then((response) => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "創建成功",
                type: "success",
                duration: 2000,
              });
              this.$emit("checkdata");
            })
            .catch(() => {});
        }
      });
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row, {
        source_state: row.source_state.id,
        dest_state: row.dest_state.id,
        workflow: this.wfdata.id,
      });
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          transition
            .requestPut(this.temp.id, this.temp)
            .then(() => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "更新成功",
                type: "success",
                duration: 2000,
              });
              this.$emit("checkdata");
            })
            .catch(() => {});
        }
      });
    },
    handleDelete(row) {
      this.$confirm("是否確定刪除?", "提示", {
        confirmButtonText: "確定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          transition.requestDelete(row.id).then(() => {
            this.$message({
              message: "刪除成功",
              type: "success",
            });
            this.$emit("checkdata");
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消刪除",
          });
        });
    },
  },
};
</script>
