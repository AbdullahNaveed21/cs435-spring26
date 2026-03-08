import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PARAMETERS
# -----------------------------
NUM_CLIENTS = 4
VECTOR_DIM = 5

# -----------------------------
# CLIENT SIDE
# -----------------------------
def generate_client_updates():
    """
    Each client generates its own update vector.
    These remain private and are not sent to the server.
    """
    updates = []
    for i in range(NUM_CLIENTS):
        vec = np.random.randint(0, 10, VECTOR_DIM)
        updates.append(vec)
    return updates


def generate_pairwise_masks():
    """
    Generate shared masks for each client pair (i,j)
    """
    masks = {}
    for i in range(NUM_CLIENTS):
        for j in range(i + 1, NUM_CLIENTS):
            masks[(i, j)] = np.random.randint(-5, 5, VECTOR_DIM)
    return masks


def create_masked_updates(updates, masks):
    """
    Each client applies masks according to rule:
    client i adds mask(i,j)
    client j subtracts mask(i,j)
    """
    masked_updates = []

    for i in range(NUM_CLIENTS):

        masked = updates[i].copy()

        for j in range(NUM_CLIENTS):

            if i < j:
                masked += masks[(i, j)]

            elif i > j:
                masked -= masks[(j, i)]

        masked_updates.append(masked)

    return masked_updates


# -----------------------------
# SERVER SIDE
# -----------------------------
def server_aggregate(masked_updates):
    """
    Server only sees masked vectors.
    It computes the aggregate.
    """
    return sum(masked_updates)


# -----------------------------
# PLOT
# -----------------------------
def save_plot(client_updates, masked_updates):
    """
    Side-by-side bar chart: private updates vs masked updates.
    Shows that masked values look noisy and hide the original signal.
    The server only ever sees the right-hand side.
    """
    x = np.arange(VECTOR_DIM)
    width = 0.18
    colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for i in range(NUM_CLIENTS):
        axes[0].bar(x + i * width, client_updates[i], width, label=f"Client {i+1}", color=colors[i])
        axes[1].bar(x + i * width, masked_updates[i], width, label=f"Client {i+1}", color=colors[i])

    axes[0].set_title("Private Updates (never seen by server)\n[Synthetic Data]")
    axes[0].set_xlabel("Vector Dimension")
    axes[0].set_ylabel("Value")
    axes[0].set_xticks(x + width * 1.5)
    axes[0].set_xticklabels([f"d{i+1}" for i in range(VECTOR_DIM)])
    axes[0].legend()

    axes[1].set_title("Masked Updates (what server receives)")
    axes[1].set_xlabel("Vector Dimension")
    axes[1].set_ylabel("Value")
    axes[1].set_xticks(x + width * 1.5)
    axes[1].set_xticklabels([f"d{i+1}" for i in range(VECTOR_DIM)])
    axes[1].legend()

    fig.suptitle("Secure Aggregation: Private vs Masked Updates", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("aggregation_plot.png", dpi=150)
    plt.close()
    print("\nPlot saved to aggregation_plot.png")




# -----------------------------
# MAIN SIMULATION
# -----------------------------
def main():

    lines = []

    def log(text=""):
        print(text)
        lines.append(text)

    log("SECURE AGGREGATION SIMULATION")
    log("(All client data below is synthetic)")
    log()

    # print("SECURE AGGREGATION SIMULATION\n")

    #Step 1: clients create updates
    client_updates = generate_client_updates()

    log("Client Updates (PRIVATE)")
    for i, u in enumerate(client_updates):
        log(f"Client {i+1}: {u}")

    # Step 2: generate masks
    masks = generate_pairwise_masks()

    # Step 3: clients send masked updates
    masked_updates = create_masked_updates(client_updates, masks)

    log("\nMasked Updates Sent To Server")
    for i, m in enumerate(masked_updates):
        log(f"Client {i+1}: {m}")

    # Step 4: server computes aggregate
    secure_sum = server_aggregate(masked_updates)

    log("\nServer Secure Aggregate")
    log(str(secure_sum))

    # Step 5: validation (not visible to server)
    plain_sum = sum(client_updates)

    log("\nPlain Sum (for validation)")
    log(str(plain_sum))

    # Step 6: correctness check
    log("\nCorrectness Check:")
    log(str(np.allclose(secure_sum, plain_sum)))

    # Save output to file
    with open("output.txt", "w") as f:
        f.write("\n".join(lines))
    print("\nOutput saved to output.txt")

    # Save plot
    save_plot(client_updates, masked_updates)


if __name__ == "__main__":
    main()