new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data() {
        return {
            filtersousjacent: 'CAC 40',
            filtermaturitydays: [30],
            filterperf: true,
            filterissuers: ['SG', 'UC'],
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
                        if (!this.filtersousjacent) {
                            return true
                        }
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
            maturitydays: [30, 60, 90, 120, 150],
            issuers: [{ key: 'SG', name: 'Société Générale' }, { key: 'UC', name: 'Unicredit' }],
            warrants: [],
            portfolio: []
        }
    },
    computed: {
        filteredWarrants() {
            // émetteurs
            var warrants0 = this.warrants.filter(warrant => this.filterissuers.includes(warrant['issuer']));
            // stratégies perf
            if (this.filterperf) {
                warrants0 = warrants0.filter(warrant =>
                    warrant['perf max'] > 8 &&
                    warrant['perf min'] > 15 &&
                    warrant['perf min'] > warrant['perf max']);
            }
            // Maturité jours
            var minVal = Math.min.apply(Math, this.filtermaturitydays) - 30;
            var maxVal = Math.max.apply(Math, this.filtermaturitydays);
            //console.log('min '+minVal+' max '+maxVal)
            warrants0 = warrants0.filter(warrant =>
                minVal < warrant['maturite jours'] && warrant['maturite jours'] < maxVal);

            return warrants0;
        },
        portfolioWarrants() {
            return this.warrants.filter(warrant => this.portfolio.filter(short => warrant['isin'].endsWith(short)).length > 0);
        },
        sousjacents() {
            var sousjacents0 = this.filteredWarrants.map(warrant => warrant['sous-jacent']);
            sousjacents0 = sousjacents0.filter((x, i, a) => a.indexOf(x) == i);
            sousjacents0.unshift('');
            return sousjacents0;
        },
        dates() {
            var now = new Date();
            var dates = [];
            for (var i = 0; i < 7; i++) {
                var date = {
                    year: now.getYear() + 1900,
                    month: String(now.getMonth() + 1).padStart(2, '0'),
                    date: String(now.getDate()).padStart(2, '0')
                }
                date.string = date.year + '-' + date.month + '-' + date.date;
                dates.push(date);
                now.setDate(now.getDate() - 1);
            }
            console.log(dates);
            return dates;
        }
    },
    methods: {
        bourso: function (item) {
            var prefix = item.issuer == 'SG' ? '3rP' : '2rP';
            return 'https://www.boursorama.com/bourse/produits-de-bourse/cours/stability-warrants/' + prefix + item.isin
        },
        url: function (date) {
            var url = 'https://testqle.s3.nl-ams.scw.cloud/json/%Y/%m/stabilitywarrants-%Y-%m-%d.json';
            url = url.replaceAll('%Y', date.year);
            url = url.replaceAll('%m', date.month);
            url = url.replaceAll('%d', date.date);
            return url;
        },
        parsedate: function (str) {
            var parts = str.split('-');
            date = {
                year: parts[0],
                month: parts[1],
                date: parts[2],
            };
            date.string = date.year + '-' + date.month + '-' + date.date;
            return date;

        },
        portfoliocodes: function () {
            return this.portfolioWarrants.map(warrant => warrant['isin']).join();
        },
        portfolioshortcodes: function () {
            return this.portfolioWarrants.map(warrant => warrant['isin']).map(isin => isin.substring(7)).join();
        }

    },
    mounted() {
        var urlParams = new URLSearchParams(window.location.search);
        // date
        var date = urlParams.get('date') == null ? this.dates[0] : this.parsedate(urlParams.get('date'));
        console.log('date=' + date.string)
        // portfolio
        this.portfolio = urlParams.get('portfolio') == null ? [] : urlParams.get('portfolio').split(',');
        console.log('portfolio=' + this.portfolio);
        // retrieve stability warrants
        var url = this.url(date);
        fetch(url)
            .then(response => response.json())
            .then(data => {
                this.warrants = data;
            });
    }
})
