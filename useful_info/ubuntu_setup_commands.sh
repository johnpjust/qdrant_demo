# Update package information
sudo apt-get update

# Install necessary packages
sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev libgdbm-dev libnss3-dev git

# Install pyenv
curl https://pyenv.run | bash

# Add pyenv and local bin to PATH in ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Apply changes to the current shell session
source ~/.bashrc

# Install specific Python version using pyenv
pyenv install 3.11.0
pyenv global 3.11.0

# Ensure pip is installed
pyenv exec python -m ensurepip
pyenv exec python -m pip install --upgrade pip

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install Docker using the convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add the current user to the Docker group to manage Docker as a non-root user
sudo usermod -aG docker $USER

# Install the latest version of Docker Compose
LATEST_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)
sudo curl -L "https://github.com/docker/compose/releases/download/$LATEST_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Check Docker and Docker Compose versions to verify installations
docker --version
docker-compose --version

# Apply the new Docker group membership
newgrp docker

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs

# Clone the Qdrant demo repository
#git clone https://github.com/qdrant/qdrant_demo.git
git clone https://github.com/johnpjust/qdrant_demo/

# Navigate to the qdrant_demo directory
cd qdrant_demo/

# checkout the relevant branch
git checkout johnpjust-ubuntu-24

# Restore potentially missing files (if applicable)
# git restore .dockerignore docker-compose-local.yaml docker-compose.yaml

# Download the demo data
wget https://storage.googleapis.com/generall-shared-data/startups_demo.json -P data/

# Set the poetry environment to use the pyenv Python version
poetry env use $(pyenv which python)

# Install Python dependencies
poetry install

# Navigate to frontend directory and install npm dependencies
cd frontend
npm install

## Fix TypeScript error by updating src/theme/index.tsx
#cat << 'EOF' > src/theme/index.tsx
#import { CSSObject, MantineThemeOverride } from "@mantine/core";
#import { heights, sizing, widths } from "./sizing";
#
#const globalStyles = (): CSSObject => ({
#  "#root": {
#    overflow: "auto",
#    display: "block",
#    width: widths.screen,
#    height: heights.screen,
#    backgroundColor: "#F2F6FF",
#    fontFamily: "Roboto,Roboto Mono",
#  },
#});
#
#const myTheme: MantineThemeOverride = {
#  globalStyles,
#  defaultRadius: "md",
#  fontFamily: "Roboto,Roboto Mono",
#  colors: {
#    Primary: ["#FFC2D6", "#F5587F", "#DC244C", "#A31030", "#660223"],
#    P500: ["#DC244C"],
#    secondary: ["#724CEF", "#148BF4", "#009999"],
#    blue: [
#      "#E7F5FF", "#D0EBFF", "#A5D8FF", "#74C0FC", "#4DABF7", "#339AF0",
#      "#148BF4", "#228BE6", "#1C7ED6", "#1971C2"
#    ],
#    purple: ["#724CEF"],
#    teal: ["#009999"],
#    Neutral: [
#      "#F2F6FF", "#DCE4FA", "#AEBDE5", "#8B9CCC", "#6A80BD", "#5069AD",
#      "#39508F", "#1F3266", "#102252", "#06153D"
#    ],
#    N500: ["#5069AD"],
#    Error: ["#FED6D6", "#F03030", "#661414"],
#    E500: ["#F03030"],
#    Success: ["#D1FADF", "#12B765", "#085232"],
#    S500: ["#12B765"],
#    Warning: ["#FEE4C7", "#F5870A", "#662F0A"],
#    W500: ["#F5870A"],
#    pink: [
#      "#FFF0F6", "#FFDEEB", "#FCC2D7", "#FAA2C1", "#F783AC", "#F06595",
#      "#DC244C", "#D6336C", "#C2255C", "#A61E4D"
#    ],
#  },
#  primaryColor: "Primary",
#  spacing: { xxs: "0.2rem" },
#  other: {
#    sizing, heights, widths,
#    fontWeights: {
#      thin: 100, extraLight: 200, light: 300, normal: 400, medium: 500,
#      semibold: 600, bold: 700, extrabold: 800, black: 900
#    },
#    subheading: {
#      sizes: {
#        SH18: { fontSize: "1.125rem", lineHeight: "1.5rem" },
#        SH12: { fontSize: "0.75rem", lineHeight: "1.125rem" }
#      }
#    },
#    paragraph: {
#      sizes: {
#        P24: { fontSize: "1.5rem", lineHeight: "2rem" },
#        P18: { fontSize: "1.125rem", lineHeight: "1.6875rem", fontWeight: 400 },
#        P16: { fontSize: "1rem", lineHeight: "1.5rem" },
#        P14: { fontSize: "0.875rem", lineHeight: "1.3125rem", fontWeight: 400 },
#        P12: { fontSize: "0.75rem", lineHeight: "1.125rem" }
#      }
#    }
#  }
#};
#
#export default myTheme;
#EOF

# Build the frontend project
npm run build

# Navigate back to the root directory
cd ..

# Start Docker containers
docker-compose -f docker-compose-local.yaml up --build -d # --build only necessary if you want to rebuild the containers

# Initialize the collection
# poetry run python -m qdrant_demo.init_collection_startups

# make the script executable
# chmod +x setup_environment.sh

# run the script
# ./setup_environment.sh

############################################### other useful commands ######################
# docker stop qdrant_demo_web qdrant_demo_qdrant && docker rm qdrant_demo_web qdrant_demo_qdrant
# docker image prune -f