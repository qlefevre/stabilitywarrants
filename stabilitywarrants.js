new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data() {
    return {
      filtersousjacent: 'CAC 40',
      filtermaturitydays: '30',
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
        {
          text: 'Maturité jours', value: 'maturite jours',
          filter: value => {
            if (!this.filtermaturitydays) return true
            filterval = parseInt(this.filtermaturitydays)
            return value < filterval & value > (filterval - 30)
          }
        },
        { text: 'Plage', value: 'plage' },
        { text: 'Cible', value: 'cible' },
        { text: 'Ecart cible abs', value: 'ecart cible abs' },
        { text: 'Perf min %', value: 'perf min' },
        { text: 'Perf max %', value: 'perf max' }
      ],
      sousjacents: [],
      warrants: [],
    }
  },
  methods: {
    bourso: function (isin) {
      var prefix = isin.startsWith('DE000SF') ? '3rP' : '2rP';
      return 'https://www.boursorama.com/bourse/produits-de-bourse/cours/stability-warrants/' + prefix + isin
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
        this.sousjacents = this.warrants.map(warrant => warrant['sous-jacent']);
        // unicité
        this.sousjacents = this.sousjacents.filter((x, i, a) => a.indexOf(x) == i);
      });
  }
})