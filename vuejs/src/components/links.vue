<template>
  <v-col cols="12">
    <h1 class="text-subtitle-1">
      <v-icon color="gray darken-2">{{ icon }}</v-icon
      >&nbsp;{{ title }}
    </h1>
    <div class="day-links">
      <v-btn v-for="(date, index) in value" :value="date" :key="index" rounded>
        <a :href="link(date, index)">
          {{ date.string }}
        </a>
        <v-icon dense @click="copy(date, index)">mdi-content-copy</v-icon>
      </v-btn>
    </div>
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
    link: function (date, index) {
      return (
        "index.html" +
        (index == 0 && !this.data ? "" : "?") +
        (index == 0 ? "" : "date=" + date.string) +
        (index != 0 && this.data ? "&" : "") +
        (this.data ? "portfolio=" + this.portfoliocodes(false) : "")
      );
    },
    copy: function (date, index) {
      var text = window.location.href + "/" + this.link(date, index);
      //console.log(text);
      navigator.clipboard.writeText(text);
    },
  },
};
</script>

<style>
.day-links .v-btn {
  margin-left: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
}
.day-links .v-btn a {
  color: inherit;
  text-decoration: inherit;
}
.day-links .v-icon {
  margin-left: 10px;
}
</style>
