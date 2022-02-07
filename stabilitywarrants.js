new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data() {
    return {
      filtersousjacent: 'CAC 40',
      filtermaturitydays: '30',
      filterperf: true,
      headers: [
        {
          text: 'Isin',
          align: 'start',
          sortable: false,
          value: 'isin',
        },
        {
          text: 'Sous-jacent', value: 'sous-jacent',
          filter: value => {
            if (!this.filtersousjacent) return true
            return this.filtersousjacent == value
          }
        },
        { text: 'Borne basse', value: 'borne basse' },
        { text: 'Borne haute', value: 'borne haute' },
        { text: 'Maturité', value: 'maturite' },
        { text: 'Maturité jours', value: 'maturite jours' },
        { text: 'Plage', value: 'plage' },
        { text: 'Cible', value: 'cible' },
        { text: 'Ecart cible abs', value: 'ecart cible abs' },
        { text: 'Perf min %', value: 'perf min' },
        { text: 'Perf max %', value: 'perf max' }
      ],
      warrants: [],
    }
  },
  computed: {
    filteredWarrants() {
      var warrants0 = this.warrants;
      if (this.filterperf) {
        warrants0 = warrants0.filter(warrant =>
          warrant['perf max'] > 8 &&
          warrant['perf min'] > 15 &&
          Fwarrant['perf min'] > warrant['perf max']);
      }
      if (this.filtermaturitydays != '') {
        var filterval = parseInt(this.filtermaturitydays)
        warrants0 = warrants0.filter(warrant =>
          warrant['maturite jours'] < filterval &
          warrant['maturite jours'] > (filterval - 30));
      }
      return warrants0;
    },
    sousjacents() {
      var sousjacents0 = this.filteredWarrants.map(warrant => warrant['sous-jacent']);
      sousjacents0 = sousjacents0.filter((x, i, a) => a.indexOf(x) == i);
      sousjacents0.unshift('');
      return sousjacents0;
    }
  },
  methods: {
    bourso: function (item) {
      var prefix = item.issuer == 'SG' ? '3rP' : '2rP';
      return 'https://www.boursorama.com/bourse/produits-de-bourse/cours/stability-warrants/' + prefix + item.isin
    }
  },
  mounted() {
    var url = 'https://testqle.s3.nl-ams.scw.cloud/json/%Y/%m/stabilitywarrants-%Y-%m-%d.json';
    var now = new Date();
    url = url.replaceAll('%Y', now.getYear() + 1900);
    url = url.replaceAll('%m', String(now.getMonth() + 1).padStart(2, '0'));
    url = url.replaceAll('%d', String(now.getDate()).padStart(2, '0'));

    fetch(url)
      .then(response => response.json())
      .then(data => {
        this.warrants = data;
      });
  }
})