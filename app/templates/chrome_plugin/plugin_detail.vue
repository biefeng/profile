{%raw%}
<template id="sample">

    <div class="plugin-detail-container">
        <div style="width: 440px;margin: auto">
            <el-carousel>
                <el-carousel-item v-for="item in 4" :key="item">
                    <img :src="plugin.cover_image"/>
                </el-carousel-item>
            </el-carousel>
        </div>
        <div class="plugin-detail-description">
            <div style="width: 100%;text-align: right;padding-right: 30px">
                <el-button @click="download(plugin.crx_url)" type="primary">下载</el-button>

            </div>
            <div style="white-space: pre-line;font-size: 16px;line-height: 24px;">
                <div style="">{{ plugin.name }}</div>
                <div style="font-weight: bolder;">{{ plugin.short_desc }}</div>
                <div style="font-weight: 300;">{{ plugin.description }}</div>
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
                    this.plugin = res.data
                })
            },
            download(url, filename) {
                let element = document.createElement("a");
                element.href = url
                // element.download = filename
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
                this.$http.get("/download-count/" + this.id).then(res => {
                    //
                })
            }
        }
    });
</script>
<style>
    .plugin-detail-container {
        height: 100%;
        padding-bottom: 10px;
        background-color: #f0f0f0;
    }

    .plugin-detail-description {
        text-align: left;
        margin: 0px 50px 0px 50px;
    }
</style>

