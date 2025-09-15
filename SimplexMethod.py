import numpy as np
from fractions import Fraction


class SimplexSolver:
    def __init__(self, c, A, b):
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        
        # Number of variables and constraints
        self.m, self.n = self.A.shape
        
        # Create the initial tableau
        self.tableau = self._create_initial_tableau()
        self.basic_vars = list(range(self.n, self.n + self.m))  # Initially slack variables are basic
        
    def _create_initial_tableau(self):
        """Create the initial simplex tableau."""
        # Add slack variables (identity matrix)
        A_with_slack = np.hstack([self.A, np.eye(self.m)])
        
        # Create the tableau
        # Last row is the objective function row (negated for maximization)
        tableau = np.zeros((self.m + 1, self.n + self.m + 1))
        
        # Fill constraint rows
        tableau[:-1, :-1] = A_with_slack
        tableau[:-1, -1] = self.b
        
        # Fill objective function row (negate for maximization)
        tableau[-1, :self.n] = -self.c
        
        return tableau
    
    def _find_pivot_column(self):
        """Find the entering variable (most negative in objective row)."""
        obj_row = self.tableau[-1, :-1]
        min_val = np.min(obj_row)
        if min_val >= 0:
            return None  # Optimal solution found
        return np.argmin(obj_row)
    
    def _find_pivot_row(self, pivot_col):
        
        rhs = self.tableau[:-1, -1]
        col = self.tableau[:-1, pivot_col]
        
        # Only consider positive ratios
        ratios = []
        for i in range(len(rhs)):
            if col[i] > 0:
                ratios.append(rhs[i] / col[i])
            else:
                ratios.append(float('inf'))
        
        min_ratio = min(ratios)
        if min_ratio == float('inf'):
            raise ValueError("Problem is unbounded")
        
        return ratios.index(min_ratio)
    
    def _pivot(self, pivot_row, pivot_col):
        # Update basic variables
        self.basic_vars[pivot_row] = pivot_col
        
        # Make pivot element 1
        pivot_element = self.tableau[pivot_row, pivot_col]
        self.tableau[pivot_row] /= pivot_element
        
        # Make other elements in pivot column 0
        for i in range(len(self.tableau)):
            if i != pivot_row and self.tableau[i, pivot_col] != 0:
                multiplier = self.tableau[i, pivot_col]
                self.tableau[i] -= multiplier * self.tableau[pivot_row]
    
    def solve(self):
        iteration = 0
        print("Initial Tableau:")
        self._print_tableau()
        
        while True:
            iteration += 1
            print(f"\nIteration {iteration}:")
            
            # Find entering variable
            pivot_col = self._find_pivot_column()
            if pivot_col is None:
                print("Optimal solution found!")
                break
            
            print(f"Entering variable: {'x' + str(pivot_col + 1) if pivot_col < self.n else 's' + str(pivot_col - self.n + 1)}")
            
            # Find leaving variable
            pivot_row = self._find_pivot_row(pivot_col)
            leaving_var = self.basic_vars[pivot_row]
            print(f"Leaving variable: {'x' + str(leaving_var + 1) if leaving_var < self.n else 's' + str(leaving_var - self.n + 1)}")
            
            # Perform pivot operation
            self._pivot(pivot_row, pivot_col)
            
            print("After pivoting:")
            self._print_tableau()
        
        return self._get_solution()
    
    def _print_tableau(self):
        """Print the current tableau in a readable format."""
        print("\nTableau:")
        # Create headers with x1, x2, s1, s2, s3, s4, RHS
        headers = []
        for i in range(self.n):
            headers.append(f"x{i+1}")
        for i in range(self.m):
            headers.append(f"s{i+1}")
        headers.append("RHS")
        
        # Print headers
        print("Basic Var |", " ".join(f"{h:>8}" for h in headers))
        print("-" * (10 + 9 * len(headers)))
        
        # Print constraint rows
        for i in range(self.m):
            if self.basic_vars[i] < self.n:
                basic_var = f"x{self.basic_vars[i] + 1}"
            else:
                basic_var = f"s{self.basic_vars[i] - self.n + 1}"
            row_str = f"{basic_var:>9} |"
            for j in range(len(self.tableau[i])):
                row_str += f"{self.tableau[i, j]:>8.2f}"
            print(row_str)
        
        # Print objective row
        row_str = f"{'z':>9} |"
        for j in range(len(self.tableau[-1])):
            row_str += f"{self.tableau[-1, j]:>8.2f}"
        print(row_str)
        print()
    
    def _get_solution(self):
        """Extract the optimal solution from the final tableau."""
        solution = np.zeros(self.n)
        
        # Get values of basic variables
        for i, var in enumerate(self.basic_vars):
            if var < self.n:  # Only original variables
                solution[var] = self.tableau[i, -1]
        
        # Objective value
        obj_value = self.tableau[-1, -1]
        
        return solution, obj_value


def solve_given_problem():
    """Solve the specific problem given in the assignment."""
    print("Solving the Linear Programming Problem:")
    print("Max z = 4x1 + 3x2")
    print("Subject to:")
    print("    x1 + x2 ≤ 8")
    print("    2x1 + x2 ≤ 10")
    print("    x1 + 3x2 ≤ 15")
    print("    2x1 + 2x2 ≤ 20")
    print("    x1, x2 ≥ 0")
    print("=" * 50)
    
    # Objective function coefficients (to maximize)
    c = [4, 3]
    
    # Constraint matrix
    A = [
        [1, 1],   # x1 + x2 ≤ 8
        [2, 1],   # 2x1 + x2 ≤ 10
        [1, 3],   # x1 + 3x2 ≤ 15
        [2, 2]    # 2x1 + 2x2 ≤ 20
    ]
    
    # Right-hand side values
    b = [8, 10, 15, 20]
    
    # Create and solve
    solver = SimplexSolver(c, A, b)
    solution, obj_value = solver.solve()
    
    # Display results
    print("\n" + "=" * 50)
    print("OPTIMAL SOLUTION:")
    print("=" * 50)
    for i, val in enumerate(solution):
        print(f"x{i+1} = {val:.4f}")
    print(f"\nMaximum value of z = {obj_value:.4f}")
    
    # Verify the solution
    print("\n" + "=" * 50)
    print("VERIFICATION:")
    print("=" * 50)
    print("Constraint checks:")
    
    constraints = [
        ([1, 1], 8, "x1 + x2 ≤ 8"),
        ([2, 1], 10, "2x1 + x2 ≤ 10"),
        ([1, 3], 15, "x1 + 3x2 ≤ 15"),
        ([2, 2], 20, "2x1 + 2x2 ≤ 20")
    ]
    
    for i, (coeffs, limit, desc) in enumerate(constraints):
        value = sum(coeffs[j] * solution[j] for j in range(len(solution)))
        status = "✓" if value <= limit + 1e-6 else "✗"
        print(f"{desc}: {value:.4f} ≤ {limit} {status}")
    
    print(f"\nObjective function: z = 4({solution[0]:.4f}) + 3({solution[1]:.4f}) = {obj_value:.4f}")


if __name__ == "__main__":
    solve_given_problem()
