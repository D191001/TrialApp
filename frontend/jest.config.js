module.exports = {
    testEnvironment: 'jsdom',
    moduleFileExtensions: ['js', 'vue'],
    transform: {
        '^.+\\.vue$': '@vue/vue3-jest',
        '^.+\\.js$': 'babel-jest'
    },
    transformIgnorePatterns: ['/node_modules/(?!axios)'],
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/src/$1'
    }
}
