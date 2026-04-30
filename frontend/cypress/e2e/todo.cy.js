describe('Todo tests', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user

    const taskTitle = 'Test todo'
    const youtubeURL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

    before(function () {
        // create a fabricated user from a fixture
        cy.fixture('user.json')
            .then((user) => {
                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/users/create',
                    form: true,
                    body: user
                }).then((response) => {
                    uid = response.body._id.$oid
                    name = user.firstName + ' ' + user.lastName
                    email = user.email

                    // login
                    cy.visit('http://localhost:3000')
                    cy.contains('div', 'Email Address')
                        .find('input[type=text]')
                        .type(email)
                    cy.get('form')
                        .submit()

                    // create task
                    cy.contains('div', 'Title')
                        .find('input[type=text]')
                        .type(taskTitle)
                    cy.contains('div', 'YouTube URL')
                        .find('input[type=text]')
                        .type(youtubeURL)
                    cy.get('form')
                        .submit()
                })
            })
    })

    beforeEach(function () {
        // Navigate to the task todo page for evry test
        cy.visit('http://localhost:3000')
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)
        cy.get('form')
            .submit()

        cy.get('.title-overlay')
            .click()
    })

    it('Test add valid todo item', () => {
        const todoName = 'watch vid at 2x speed'

        cy.get('.inline-form > [type="text"]')
            .type(todoName)

        cy.get('.inline-form > [type="submit"]')
            .click()

        cy.get('.todo-list .todo-item')
            .last()
            .should('contain.text', todoName)
    })

    it('Test empty description', () => {
        cy.get('.inline-form > [type="submit"]')
            .should('be.disabled')
    })

    after(function () {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})
