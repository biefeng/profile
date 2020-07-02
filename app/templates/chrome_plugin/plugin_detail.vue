{%raw%}
<template id="sample">
    <div style="height: 100%;width:100%;display: flex;justify-content: center;">
        <div style="width: 70%;height: 100%;background-color: #f0f0f0;box-shadow: 0px 0px 2px gray;text-align: center;padding: 0px;">
            <div style="width: 440px;margin: auto">
                <el-carousel>
                    <el-carousel-item v-for="item in 4" :key="item">
                        <img :src="plugin.cover_image"/>
                    </el-carousel-item>
                </el-carousel>
            </div>
            <div style="text-align: left;margin: 0px 50px 50px 50px;">
                <div style="width: 100%;text-align: right;padding-right: 30px">
                    <a :href="plugin.crx_url">
                        <el-button type="primary">下载</el-button>
                    </a>
                </div>
                <div style="white-space: pre-line;font-size: 16px;line-height: 24px;">
                    <div style="">{{ plugin.name }}</div>
                    <div style="font-weight: bolder;">{{ plugin.short_desc }}</div>
                    <div style="font-weight: 300;">{{ plugin.description }}</div>
                </div>
            </div>
        </div>
    </div>
</template>
{%endraw%}
<script>
    console.log(window.context)
    Vue.component("main-content", {
        template: "#sample",
        data() {
            return {
                message: "The is a sample component",
                id: '{{id}}', //由jinja模板去解析并赋值
                plugin: {}
            }
        },
        created() {
            this.getDetail()
        },
        methods: {
            getDetail() {
                this.$http.get("/chrome-plugin/detail-data/" + this.id).then(res => {
                    console.log(res.data)
                    this.plugin = res.data
                })
            }
        }
    });
</script>
<style>

</style>

