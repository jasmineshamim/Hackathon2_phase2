describe('Authentication Flow', () => {
  it('should allow a new user to sign up', () => {
    cy.visit('/signup');
    
    cy.get('input[placeholder="John"]').type('John');
    cy.get('input[placeholder="Doe"]').type('Doe');
    cy.get('input[placeholder="john.doe@example.com"]').type('john.doe@example.com');
    cy.get('input[type="password"]').first().type('Password123');
    cy.get('input[type="password"]').eq(1).type('Password123');
    
    cy.get('button').contains('Sign Up').click();
    
    // Should redirect to dashboard after successful signup
    cy.url().should('include', '/dashboard');
  });

  it('should allow an existing user to sign in', () => {
    cy.visit('/signin');
    
    cy.get('input[placeholder="Enter your username or email"]').type('john.doe@example.com');
    cy.get('input[placeholder="Enter your password"]').type('Password123');
    
    cy.get('button').contains('Sign In').click();
    
    // Should redirect to dashboard after successful signin
    cy.url().should('include', '/dashboard');
  });

  it('should show error for invalid credentials', () => {
    cy.visit('/signin');
    
    cy.get('input[placeholder="Enter your username or email"]').type('invalid@example.com');
    cy.get('input[placeholder="Enter your password"]').type('wrongpassword');
    
    cy.get('button').contains('Sign In').click();
    
    // Should show error message
    cy.contains('Invalid credentials').should('be.visible');
  });
});