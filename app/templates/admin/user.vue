{% raw%}
<template id="article-list">
    <div>
        <el-row :gutter="20">
            <el-col :xs="{span:15,offset:0}" :sm="{span:9,offset:0}" :md="{span:6}" :lg="{span:5}">
                <span class="query-label">来源:</span>
                <el-select v-model="query.source" placeholder="请选择">
                    <el-option
                            v-for="item in sources"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :xs="{span:15,offset:0}" :sm="{span:9,offset:0}" :md="{span:6}" :lg="{span:5}">
                <span class="query-label">分类:</span>
                <el-select v-model="query.category" placeholder="请选择">
                    <el-option
                            v-for="item in categories"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :xs="{span:15,offset:0}" :sm="{span:9,offset:0}" :md="{span:5}">
                <el-button type="primary" @click="list(1,query)">查询</el-button>
                <el-button type="danger">批量删除</el-button>
                <el-button type="success" @click="dialogVisible=!dialogVisible">添加用户</el-button>
            </el-col>
        </el-row>

        <el-table
                v-loading="loading"
                border
                :stripe="true"
                ref="multipleTable"
                :data="tableData"
                tooltip-effect="dark"
                style="width: 100%"
                @selection-change="handleSelectionChange"
        >
            <el-table-column
                    type="selection"
                    width="55">
            </el-table-column>
            <el-table-column
                    label="用户名">
                <template slot-scope="scope">{{ scope.row.username }}</template>
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="邮箱">
                <template slot-scope="scope">{{ scope.row.email }}</template>
            </el-table-column>

            <el-table-column
                    prop="address"
                    label="操作"
                    show-overflow-tooltip>
                <template slot-scope="scope">
                    <a :href="'/article/edit/'+scope.row.id">
                        <el-button
                                v-if="scope.row.source === 1"
                                size="mini">编辑
                        </el-button>
                    </a>
                    <el-button
                            size="mini"
                            type="danger"
                            @click="handleDelete(scope.$index, scope.row)">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <pagination :total="total" :size_change="sizeChange" :current_change="list"></pagination>
        <el-dialog
                title="添加用户"
                :visible.sync="dialogVisible"
                width="30%"
                :before-close="handleClose">
            <div class="input-group" style="width: auto;height: auto;margin: auto">
                <div class="input-group-field">
                    <el-input class="input-group-field-value" v-model="newUser.email" placeholder="Email"></el-input>
                </div>
                <div class="input-group-field">
                    <el-input class="input-group-field-value" v-model="newUser.username" placeholder="Username"></el-input>
                </div>
                <div class="input-group-field">
                    <el-input class="input-group-field-value" v-model="newUser.password" placeholder="Password"></el-input>
                </div>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addUser">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>
{% endraw%}
{% include 'base/pagination.vue' %}
<script>
    Vue.component("main-content", {
        template: "#article-list",
        data() {
            return {
                tableData: [],
                option: 1,
                dialogVisible: false,
                query: {},
                pageSize: 10,
                currentPage: 1,
                total: 0,
                loading: false,
                newUser: {
                    email: '',
                    username: '',
                    password: ''
                }
            }
        },
        methods: {
            handleEdit() {

            },
            handleDelete(index, row) {
                this.$http.post("/admin/user/del", {id: [row.id]}).then(res => {
                    this.list(1)
                }).catch(e => {
                    console.log(e)
                })
            },
            handleSelectionChange() {
            },
            list(pageNum, params) {
                this.loading = true
                let assign = Object.assign({pageNumber: pageNum, pageSize: this.pageSize}, params);
                if (pageNum != undefined) {
                    this.currentPage = pageNum
                }
                this.$http.get("/admin/user/list", {
                    params: assign
                }).then(res => {
                    this.tableData = res.data.list
                    this.total = res.data.total
                    this.loading = false
                }).catch(e => {
                    this.$message.error(e.message)
                    this.loading = false
                })
            },
            sizeChange(s) {
                this.pageSize = s
                this.list(0, {pageSize: s})
            },
            handleClose(done) {
                this.$confirm('确认关闭？')
                    .then(_ => {
                        done()
                    })
                    .catch(_ => {
                    });
            },
            addUser() {
                this.dialogVisible = false
                this.$http.post("/admin/user/add", this.newUser).then(res => {
                    this.$message.success("添加成功")
                    this.list(1)
                }).catch(e => {
                    this.$message.error(e.message)
                })
            }
        },
        created() {
            this.list(1)
        }
    });

</script>
<style>
    .query-label {
        padding: 0px 15px 0px 10px;
    }


    .el-col {
        border-radius: 4px;
        margin-bottom: 20px;
    }

    .input-group {
        text-align: center;
        width: calc(100vw);
        line-height: 10px;
        position: relative;
        top: 25%;
    }

    .input-group-header {
        font-size: 1.75rem;
        height: 50px;
        line-height: 50px;
        font-weight: bolder;
    }

    .input-group-field {
        margin: 0px auto;
        text-align: left;
        line-height: 60px;
        width: 400px;
        height: 60px;
    }

    .input-group-field-label {
        display: inline-block;
        height: 30px;
        text-align: left;
        width: 60px;
    }
</style>