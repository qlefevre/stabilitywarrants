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
    <!-- stability warrants -->
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

    <!-- portfolio -->
    <template slot="item.pvlatentes" slot-scope="data">
      <slot name="item.pvlatentes" v-bind="data"></slot>
    </template>
    <template slot="item.pvlatentespercentage" slot-scope="data">
      <slot name="item.pvlatentespercentage" v-bind="data"></slot>
    </template>
    <template slot="item.pvpotentielles" slot-scope="data">
      <slot name="item.pvpotentielles" v-bind="data"></slot>
    </template>
    <template slot="item.pvpotentiellespercentage" slot-scope="data">
      <slot name="item.pvpotentiellespercentage" v-bind="data"></slot>
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
