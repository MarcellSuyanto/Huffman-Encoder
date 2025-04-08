
class Node:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right


# Gets the frequencies of all the characters and symbols in {line} and stores them in {chars}
def get_count(line, chars): 
    """
    line -> str -> string of symbols and characters
    chars -> dict -> stores the frequencies of symbols and characters
    return -> None
    """
    for char in line:
        if char in chars:
            chars[char] += 1
        else:
            chars[char] = 1
    

def build_tree(leaves):
    while len(leaves) > 1:

        left = leaves.pop()
        right = leaves.pop()
        total = left[1] + right[1]

        leaves.append((Node(left[0], right[0]), total))
        leaves = sorted(leaves, key=lambda x:x[1], reverse=True)
    
    return leaves

def traverse_tree(node, string=""):
    if isinstance(node, str):
        return {node: string}
    
    codes = dict()
    l = node.left
    r = node.right

    for char, code in traverse_tree(l, string+'0').items():
        codes[char] = code
    for char, code in traverse_tree(r, string+'1').items():
        codes[char] = code
    return codes

def encode(string, codes):
    ans = ""
    for i in string:
        ans += codes[i]
    
    ans = [ans[i:i + 80] for i in range(0, len(ans), 80)]
    encodemsg = open("encodemsg.txt","w")
    for line in ans:
        encodemsg.write(line + "\n")
    encodemsg.close()

def get_code(codes, chars):
    numerator = 0
    denominator = 0

    sorted_codes = dict(sorted(codes.items(), key=lambda x:x[0]))
    with open("code.txt", 'w') as file:
        for char, code in sorted_codes.items():
            numerator += len(code)*chars[char]
            denominator += chars[char]
            out = char
            if out == " ":
                out = "Space"
            line = f"{out}: {sorted_codes[char]}\n"
            file.write(line)
        file.write(f"Ave = {round(numerator/denominator, 2)} bits per symbol")



def main():
    chars_dict = dict()
    string = ""
    with open("input.txt", "r") as file:
        for line in file:
            line = line.rstrip("\n")
            get_count(line, chars_dict)
            string += line

    # Sorts chars by descending order of character frequency
    chars = sorted(chars_dict.items(), key=lambda x:x[1], reverse=True)
    huffman_tree = build_tree(chars)
    codes = traverse_tree(huffman_tree[0][0])
    print(codes)
    encode(string, codes)
    get_code(codes, chars_dict)
    
        

main()