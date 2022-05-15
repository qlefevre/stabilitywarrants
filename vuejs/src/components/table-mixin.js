// define a mixin object
var tableMixin = {
    methods: {
        getStyle(perf) {
            if (perf < 7) return "red-value";
            else if (perf < 12) return "orange-value";
            else return "";
        },
        getPvStyle(pv) {
            if (pv < 0) return "red-pv";
            return "green-pv";
        }
    }
};