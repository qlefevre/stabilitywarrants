<template>
  <v-col>
    <h1 class="text-subtitle-1">
      <v-icon color="gray darken-2">{{ icon }}</v-icon
      >&nbsp;{{ title }}
    </h1>
    <v-chip-group label="Semaine" v-model="value" class="day-links">
      <v-chip link v-for="(date, index) in value" :value="date" :key="index">
        <a
          :href="
            'index.html' +
            (index == 0 && !data ? '' : '?') +
            (index == 0 ? '' : 'date=' + date.string) +
            (index != 0 && data ? '&' : '') +
            (data ? 'portfolio=' + portfoliocodes(false) : '')
          "
        >
          {{ date.string }}
        </a>
        <!--<v-icon small @click="copy(date)">mdi-content-copy</v-icon>-->
      </v-chip>
    </v-chip-group>
  </v-col>
</template>

<script>
module.exports = {
  props: ["value", "data", "portfolio"],
  computed: {
    icon() {
      if (this.data) {
        return "mdi-credit-card-clock";
      } else {
        return "mdi-clock-remove-outline";
      }
    },
    title() {
      if (this.data) {
        return "Par date avec compte titres";
      } else {
        return "Par date";
      }
    },
  },
  methods: {
    portfoliocodes: function (short) {
      return this.portfolio
        .map((warrant) => warrant.isin + "-" + warrant.quantite + "-" + warrant.prixrevient)
        .map((isin) => (short ? isin.substring(7) : isin))
        .join();
    },
    copy: function (date) {
      console.log("date " + date.string);
    },
  },
};
</script>

<style>
.day-links .v-icon {
  margin-left: 10px;
}
</style>