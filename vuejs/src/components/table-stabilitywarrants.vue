<template>
  <v-data-table
    :headers="this.headers"
    :items="this.items"
    :sort-by="['sous-jacent', 'plage', 'ecartcibleabs']"
    :sort-desc="[false, true, false]"
    :footer-props="{ 'items-per-page-options': [-1, 50, 100] }"
    multi-sort
    dense
    class="elevation-1"
    mobile-breakpoint="100"
  >
    <template v-slot:item.isin="{ item }">
      <isin v-model="item"></isin>
    </template>
    <template v-slot:item.perfmin="{ item }">
      <span :style="getPerfStyle(item.perfmin)">{{ item.perfmin }}</span>
    </template>
    <template v-slot:item.perfmax="{ item }">
      <span :style="getPerfStyle(item.perfmax)">{{ item.perfmax }}</span>
    </template>
  </v-data-table>
</template>

<script>
module.exports = {
  props: ["items", "headers"],
  methods: {
    getPerfStyle(perf) {
      if (perf < 7) return "color:red;font-weight:bold;";
      else if (perf < 12) return "color:orange;font-weight:bold;";
      else return "";
    },
  },
  components: {
    isin: httpVueLoader("vuejs/src/components/isin.vue"),
  },
};
</script>

<style>
</style>