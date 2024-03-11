module.exports = {
	"env": {
		"browser": true,
		"es2021": true
	},
	"extends": [
		"eslint:recommended",
		"plugin:vue/vue3-essential"
	],
	"globals":{
		"d3": true,
		"sysDatasetObj": true,
		"$": true,
		"lodash":true,
	},
	"overrides": [
		{
			"env": {
				"node": true
			},
			"files": [
				".eslintrc.{js,cjs}"
			],
			"parserOptions": {
				"sourceType": "script"
			}
		}
	],
	"parserOptions": {
		"ecmaVersion": "latest",
		"sourceType": "module"
	},
	"plugins": [
		"vue"
	],
	"rules": {


		"no-console": "warn",
      "no-alert": "warn",
      "no-unused-vars": "warn",
      "vue/valid-v-for": "warn",
      "vue/no-unused-vars": "warn",


	}
}
