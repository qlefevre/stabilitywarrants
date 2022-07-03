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
    <template v-slot:item.bornebasse="{ item }">
      {{ item.bornebasse }}
    </template>
    <template v-slot:item.bornehaute="{ item }">
      {{ item.bornehaute }}
    </template>
    <template v-slot:item.maturitejours="{ item }">
      <v-tooltip right>
        <template v-slot:activator="{ on, attrs }">
          <span v-bind="attrs" v-on="on"> {{ item.maturitejours }}</span>
        </template>
        <span>{{ maturiteJoursOuvrables(item.maturitejours) }} jours ouvrables</span>
      </v-tooltip>
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
    <template v-slot:item.pvpercentage="{ item }">
      <v-tooltip left>
        <template v-slot:activator="{ on, attrs }">
          <span v-bind="attrs" v-on="on" :class="getPvStyle(pvPercentage(item))">{{ pvPercentage(item) }}</span>
        </template>
        <span>{{ pvPercentagePerPeriod(item,30) }} / Mois</span></br>
        <span>{{ pvPercentagePerPeriod(item,365) }} / An</span>
      </v-tooltip>
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
  methods: {
    pvPercentage(warrant) {
      return ((10 / warrant.vente - 1) * 100).toFixed(2);
    },
    pvPercentagePerPeriod(warrant, days) {
      return ((this.pvPercentage(warrant) * days) / warrant.maturitejours).toFixed(2);
    },
    maturiteJoursOuvrables(maturitejours) {
      var days = maturitejours;
      if (days >= 7) {
        var weeks = Math.floor(maturitejours / 7);
        days = maturitejours - 2 * weeks;
      }
      return days;
    },
  },
};
</script>

<style src="vuejs/src/components/table.css">
</style>
