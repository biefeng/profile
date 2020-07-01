{%raw%}
<div id="sample">
    {{activeIndex1}}
</div>
{%endraw%}
<script>
    let element = document.querySelector("#sample");
    Vue.component("main-content", {
        template: element.outerHTML,
        data() {
            return {
                activeIndex1: 1
            }
        }
    });
</script>

