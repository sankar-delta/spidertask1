import random
from math import ceil
from decimal import Decimal


class ShamirSecretSharing:
    def __init__(self, prime=2 ** 127 - 1):
        """Initialize with a large prime number (default is Mersenne prime 2^127-1)"""
        self.prime = prime

    def _eval_poly(self, coeffs, x):
        """Evaluate polynomial with given coefficients at point x"""
        return sum((coeff * (x ** i) for i, coeff in enumerate(coeffs)), Decimal(0)) % self.prime

    def _generate_polynomial(self, secret, threshold):
        """Generate a random polynomial where the constant term is the secret"""
        coeffs = [Decimal(secret)]
        # Random coefficients for higher degree terms
        coeffs += [Decimal(random.randint(0, self.prime - 1))
                   for _ in range(threshold - 1)]
        return coeffs

    def generate_shares(self, secret, num_shares, threshold):
        """
        Split secret into shares using polynomial interpolation
        Args:
            secret: The secret to share (integer)
            num_shares: Total number of shares to generate (n)
            threshold: Minimum number of shares needed to reconstruct (k)
        Returns:
            List of (x, y) pairs (shares)
        """
        if threshold > num_shares:
            raise ValueError("Threshold cannot be greater than number of shares")

        # Convert secret to integer if it's not already
        secret_int = int.from_bytes(secret.encode('utf-8'), 'big') if isinstance(secret, str) else secret

        coeffs = self._generate_polynomial(secret_int, threshold)
        shares = []

        for x in range(1, num_shares + 1):
            x_val = Decimal(x)
            y_val = self._eval_poly(coeffs, x_val)
            shares.append((x, int(y_val)))

        return shares

    def reconstruct_secret(self, shares):
        """
        Reconstruct the secret from shares using Lagrange interpolation
        Args:
            shares: List of at least k shares [(x1, y1), (x2, y2), ...]
        Returns:
            The reconstructed secret (integer)
        """
        if len(shares) < 2:
            raise ValueError("Need at least 2 shares to reconstruct")

        x_coords = [Decimal(x) for x, _ in shares]
        y_coords = [Decimal(y) for _, y in shares]

        secret = Decimal(0)

        for i in range(len(shares)):
            # Compute Lagrange basis polynomial
            numerator = Decimal(1)
            denominator = Decimal(1)

            for j in range(len(shares)):
                if i == j:
                    continue
                numerator *= -x_coords[j]
                denominator *= (x_coords[i] - x_coords[j])

            # Add the contribution from this share
            secret += (numerator / denominator) * y_coords[i]

        secret = int(round(secret)) % self.prime

        # If the secret was originally a string, convert it back
        try:
            return secret.to_bytes(ceil(secret.bit_length() / 8), 'big').decode('utf-8')
        except UnicodeDecodeError:
            return secret


# Example usage
if __name__ == "__main__":
    sss = ShamirSecretSharing()

    # Example 1: Numeric secret
    secret_number = 123456789
    print(f"Original secret (number): {secret_number}")

    shares = sss.generate_shares(secret_number, num_shares=5, threshold=3)
    print(f"\nGenerated shares (5 total, need 3 to reconstruct):")
    for share in shares:
        print(f"  Share {share[0]}: {share[1]}")

    # Reconstruct with first 3 shares
    reconstructed = sss.reconstruct_secret(shares[:3])
    print(f"\nReconstructed from 3 shares: {reconstructed}")

    # Example 2: String secret
    secret_string = "My crypto wallet password"
    print(f"\nOriginal secret (string): '{secret_string}'")

    shares = sss.generate_shares(secret_string, num_shares=4, threshold=2)
    print(f"\nGenerated shares (4 total, need 2 to reconstruct):")
    for share in shares:
        print(f"  Share {share[0]}: {share[1]}")

    # Reconstruct with any 2 shares
    reconstructed = sss.reconstruct_secret(shares[1:3])
    print(f"\nReconstructed from shares 2 & 3: '{reconstructed}'")