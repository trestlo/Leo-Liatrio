resource "aws_ecr_repository" "ecr_repository" {
  name = "${var.cluster_name}-ecr-repo"
}

resource "aws_eks_cluster" "eks_cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_iam_role.arn

  vpc_config {
    security_group_ids      = [aws_security_group.eks_cluster.id, aws_security_group.eks_nodes.id]
    endpoint_private_access = true
    endpoint_public_access  = true
    subnet_ids = [aws_subnet.private_subnet[0].id, aws_subnet.private_subnet[1].id]
  }

  depends_on = [aws_iam_role_policy_attachment.eks_iam_role_attachment]
}

resource "aws_eks_node_group" "eks-nodes" {
  cluster_name    = var.cluster_name
  node_group_name = "private-nodes"
  node_role_arn   = aws_iam_role.eks_nodes.arn

  subnet_ids = [aws_subnet.private_subnet[0].id, aws_subnet.private_subnet[1].id]

  capacity_type  = "ON_DEMAND"
  instance_types = ["${var.instance_type}"]

  scaling_config {
    desired_size = 1
    max_size     = 3
    min_size     = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.nodes-AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.nodes-AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.nodes-AmazonEC2ContainerRegistryReadOnly,
  ]
}
