<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="請輸入內容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
        @clear="handleFilter"
      />
      <el-button-group>
        <el-button
          class="filter-item"
          type="primary"
          icon="el-icon-search"
          @click="handleFilter"
        >{{ "搜索" }}</el-button>
      </el-button-group>
    </div>

    <el-table
      :data="list"
      v-loading="listLoading"
      border
      style="width: 100%"
      highlight-current-row
      @sort-change="handleSortChange"
      @contextmenu.native.prevent="handleContextMenu"
    >
      <el-table-column label="名稱" prop="name"></el-table-column>
      <el-table-column label="單號" prop="sn" width="240">
        <template slot-scope="{ row }">
          <router-link :to="'/s_ticket/' + row.id">
            <el-link type="success">{{row.sn}}</el-link>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column label="申請人" prop="create_user">
        <template slot-scope="{ row }">
          <span>{{row.create_user.username}}</span>
        </template>
      </el-table-column>
      <el-table-column label="當前環節" prop="state">
        <template slot-scope="{ row }">
          <span>{{row.state.name}}</span>
        </template>
      </el-table-column>
      <el-table-column label="急件狀態" prop="transition">
        <template slot-scope="{ row }">
          <span>
            {{
              row.name.startsWith('工單')
              ? '一般'
              : (AttributeTypeFilter2(JSON.parse(row.customfield).find(item => item.field_key === 'status' || item.customfield % 10 === 8).field_value))
            }}
          </span>
        </template>
    </el-table-column>
      <el-table-column label="當前處理人" prop="participant">
        <template slot-scope="{ row }">
          <span>{{row.participant}}</span>
        </template>
      </el-table-column>
      <el-table-column label="創建日期" prop="create_time"></el-table-column>
      <!-- <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              v-if="true"
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >{{ "刪除" }}</el-button>
          </el-button-group>
        </template>
      </el-table-column> -->
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              size="small"
              icon="el-icon-arrow-up"
              @click.stop="handleCommand({ action: 'moveUp', row })"
            >上移</el-button>
            <el-button
              size="small"
              icon="el-icon-arrow-down"
              @click.stop="handleCommand({ action: 'moveDown', row })"
            >下移</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-pagination">
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>
  </div>
</template>

<script>
import { ticket, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
// import { AttributeTypeFilter2 } from "@/filters";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";
import { mapGetters } from "vuex";

export default {
  name: "my_ticket",

  components: { Pagination },
  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false
      },
      list: [],
      total: 0,
      listLoading: true,
      loading: true,
      listQuery: {
        page: 1,
        limit: 20,
        search: undefined,
        ordering: undefined,
        create_user__username: this.username
      },
      contextMenuVisible: false,
      contextMenuTop: '0px',
      contextMenuLeft: '0px',
      selectedRow: null
    };
  },
  computed: {
    ...mapGetters(["username"])
  },
  created() {
    this.getMenuButton();
    this.getList();
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
        .requestMenuButton("my_ticket")
        .then(response => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      this.listQuery.create_user__username =  this.username
      ticket.requestGet(this.listQuery).then(response => {
        this.list = response.results;
        // 如果 localStorage 中有保存的列表順序，則按照這個順序對列表進行排序
        const listOrder = JSON.parse(localStorage.getItem('myTicketListOrder'));
        if (listOrder) {
          this.list.sort((a, b) => listOrder.indexOf(a.id) - listOrder.indexOf(b.id));
        }
        this.total = response.count;
        this.listLoading = false;
      });
    },
    handleFilter() {
      this.getList();
    },
    handleSortChange(val) {
      if (val.order === "ascending") {
        this.listQuery.ordering = val.prop;
      } else if (val.order === "descending") {
        this.listQuery.ordering = "-" + val.prop;
      } else {
        this.listQuery.ordering = "";
      }
      this.getList();
    },
    handleDelete(row) {
      this.$confirm("是否確定刪除?", "提示", {
        confirmButtonText: "確定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          ticket.requestDelete(row.id).then(() => {
            this.$message({
              message: "刪除成功",
              type: "success"
            });
            this.getList();
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消刪除"
          });
        });
    },
    handleContextMenu(event) {
        this.contextMenuVisible = true;
        this.contextMenuTop = event.clientY + 'px';
        this.contextMenuLeft = event.clientX + 'px';
        event.stopPropagation();
        event.preventDefault();
      },
      handleCommand(command) {
        this.selectedRow = command.row;
  
        if (command.action === 'moveUp') {
          this.moveUp();
        } else if (command.action === 'moveDown') {
          this.moveDown();
        }
      },
      moveUp() {
        const index = this.list.indexOf(this.selectedRow);
        if (index > 0) {
          const temp = this.list[index];
          this.list.splice(index, 1);
          this.list.splice(index - 1, 0, temp);
        }
        // 將當前的列表順序保存到 localStorage
        localStorage.setItem('myTicketListOrder', JSON.stringify(this.list.map(item => item.id)));
      },
      moveDown() {
        const index = this.list.indexOf(this.selectedRow);
        if (index < this.list.length - 1) {
          const temp = this.list[index];
          this.list.splice(index, 1);
          this.list.splice(index + 1, 0, temp);
        }
        // 將當前的列表順序保存到 localStorage
        localStorage.setItem('myTicketListOrder', JSON.stringify(this.list.map(item => item.id)));
      },
      AttributeTypeFilter2(val) {
        const Map = {
          1: '一般',
          2: '急件',
          3: '特急件'
        }
        return Map[val]
      }
  }
};
</script>
