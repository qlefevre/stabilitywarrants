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
    <template v-slot:item.bornes="{ item }"> {{ item.bornebasse }} {{ item.bornehaute }} </template>
    <template v-slot:item.pvlatentes="{ item }">
      <span :class="getPvStyle(item.pvlatentes)">{{ item.pvlatentes }}</span>
    </template>
    <template v-slot:item.pvlatentespercentage="{ item }">
      <span :class="getPvStyle(item.pvlatentespercentage)">{{ item.pvlatentespercentage }}</span>
    </template>
    <template v-slot:item.pvpotentielles="{ item }">
      <span :class="getPvStyle(item.pvpotentielles)">{{ item.pvpotentielles }}</span>
    </template>
    <template v-slot:item.pvpotentiellespercentage="{ item }">
      <span :class="getPvStyle(item.pvpotentiellespercentage)">{{ item.pvpotentiellespercentage }}</span>
    </template>

    <template slot="item.actions" slot-scope="data">
      <slot name="item.actions" v-bind="data"></slot>
    </template>

    <template slot="group.header" slot-scope="data">
      <slot name="group.header" v-bind="data"></slot>
    </template>
  </v-data-table>
</template>

<script>
module.exports = {
  props: ["items", "headers"],
  mixins: [tableMixin],
  components: {
    isin: httpVueLoader("vuejs/src/components/isin.vue"),
  },
};
</script>

<style src="vuejs/src/components/table.css">
</style>
