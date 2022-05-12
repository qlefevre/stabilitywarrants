<template>
  <v-data-table
    :headers="this.headers"
    :items="this.items"
    v-bind="$attrs"
    multi-sort
    dense
    class="elevation-1"
    mobile-breakpoint="100"
  >
    <template v-slot:item.isin="{ item }">
      <isin v-model="item"></isin>
    </template>
    <template v-slot:item.perfmin="{ item }">
      <span :class="getStyle(item.perfmin)">{{ item.perfmin }}</span>
    </template>
    <template v-slot:item.perfmax="{ item }">
      <span :class="getStyle(item.perfmax)">{{ item.perfmax }}</span>
    </template>

    <template v-slot:item.bornes="{ item }">
      {{ item.bornebasse }} {{ item.bornehaute }}
    </template>
    <template v-slot:item.pvlatentes="{ item }">
      <span :class="getPvStyle(item.pvlatentes)">{{ item.pvlatentes }}</span>
    </template>
    <template v-slot:item.pvpotentielles="{ item }">
      <span :class="getPvStyle(item.pvpotentielles)">{{
        item.pvpotentielles
      }}</span>
    </template>

    <template slot="group.header" slot-scope="data">
      <slot name="group.header" v-bind="data"></slot>
    </template>
  </v-data-table>
</template>

<script>
module.exports = {
  props: ["items", "headers"],
  methods: {
    getStyle(perf) {
      if (perf < 7) return "red-value";
      else if (perf < 12) return "orange-value";
      else return "";
    },
    getPvStyle(pv) {
      if (pv < 0) return "red-pv";
      return "green-pv";
    },
  },
  components: {
    isin: httpVueLoader("vuejs/src/components/isin.vue"),
  },
};
</script>

<style>
@import "table.css";
</style>